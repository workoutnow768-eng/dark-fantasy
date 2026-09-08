"""
Orchestrator for the dark-fantasy video pipeline. Runs headlessly in
GitHub Actions -- generates a still + silent video per scene via
Higgsfield's REST API, muxes the page's music track on with ffmpeg, and
schedules posts via Buffer's GraphQL API.

Same two-phase split as auto-post7, for the same reason: Buffer needs to
fetch the final .mp4 from its public raw.githubusercontent.com URL, which
only exists once the committed file is pushed.

  generate: generates today's N scenes (still -> video -> mux), writes a
            manifest.json listing the final video paths + captions +
            scheduled times. The workflow then commits + pushes these.
  schedule: reads the manifest (now live on raw.githubusercontent.com) and
            creates the Buffer posts, then updates state and bumps the
            rotation index + music offset.

Usage: python scripts/main.py generate
       python scripts/main.py schedule
"""
import os
import sys
import json
import datetime

sys.path.insert(0, os.path.dirname(__file__))

import higgsfield_client
import buffer_client
import mux_audio
from scene_bank import SCENES

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STATE_PATH = os.path.join(REPO_ROOT, "state", "dark_fantasy_state.json")
OUTPUT_SUBDIR = "output/dark_fantasy"

# Same three channels for this account as the recipe pipeline, plus
# YouTube -- which recipe couldn't use because it only ever produced
# image carousels (Buffer requires real video content for YouTube).
CHANNELS = ["ai_facts4u", "daily_ai_factz", "Factual days"]
BUFFER_TOKEN_ENV = "BUFFER_ACCESS_TOKEN_DARKFANTASY"

CAPTION = ""  # deliberately empty -- the page is silent-visual/vibes only, no on-screen text and no caption copy per dez
HASHTAGS = "#darkfantasy #fantasyart #gothic #medievalfantasy #aiart"


def manifest_path():
    return os.path.join(REPO_ROOT, OUTPUT_SUBDIR, "manifest.json")


def load_state():
    with open(STATE_PATH) as f:
        return json.load(f)


def save_state(state):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


def raw_url(repo_relative_path):
    repo = os.environ.get("GITHUB_REPOSITORY")  # "owner/repo"
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    if not repo:
        raise RuntimeError("GITHUB_REPOSITORY env var not set -- are you running outside GitHub Actions?")
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{repo_relative_path}"


def next_scheduled_times(state, count):
    slots = state["daily_time_slots_uk"]
    last = datetime.datetime.fromisoformat(state["scheduled_up_to"].replace("Z", "+00:00"))
    day = last.date() + datetime.timedelta(days=1)
    times = []
    for i in range(count):
        slot = slots[i % len(slots)]
        hh, mm = [int(x) for x in slot.split(":")]
        dt = datetime.datetime(day.year, day.month, day.day, hh, mm, tzinfo=datetime.timezone.utc)
        times.append(dt)
        if (i + 1) % len(slots) == 0:
            day = day + datetime.timedelta(days=1)
    return times


def phase_generate():
    state = load_state()
    posts_per_day = state.get("posts_per_day", 3)
    count = posts_per_day
    start_index = state["last_scene_index"] + 1

    scheduled_times = next_scheduled_times(state, count)
    today_tag = datetime.datetime.utcnow().strftime("%Y%m%d")
    music_url = os.environ["MUSIC_TRACK_URL"]
    music_local_path = os.path.join(REPO_ROOT, ".cache_music.mp3")

    # Download the page's music track once per run (not once per scene) --
    # cheap either way, but no reason to refetch it 3x.
    import requests as _requests
    resp = _requests.get(music_url, timeout=60)
    resp.raise_for_status()
    with open(music_local_path, "wb") as f:
        f.write(resp.content)

    scenes_meta = []
    scenes_to_generate = []
    out_dirs = []
    for i in range(count):
        scene_index = (start_index + i) % len(SCENES)
        scene = SCENES[scene_index]
        item_out_dir = os.path.join(REPO_ROOT, OUTPUT_SUBDIR, f"{today_tag}_{i+1}_{scene['title'].replace(' ', '_')}")
        os.makedirs(item_out_dir, exist_ok=True)
        scenes_meta.append({"scene": scene, "scene_index": scene_index, "out_dir": item_out_dir})
        scenes_to_generate.append(scene)
        out_dirs.append(item_out_dir)

    print(f"[INFO] Generating {count} still+video scenes (up to 3 concurrent)...")
    results, errors = higgsfield_client.generate_posts_concurrent(scenes_to_generate, out_dirs, max_workers=3)

    # Same safety rule as auto-post7: an nsfw block on one scene is a
    # normal per-scene safety event (skip it), but any other failure
    # (bad credentials, 0 credits, API outage) is systemic and should stop
    # the whole run loudly rather than silently posting broken/missing
    # content to a live audience.
    hard_failures = [
        (i, err) for i, err in enumerate(errors)
        if err is not None and not isinstance(err, higgsfield_client.GenerationBlocked)
    ]
    if hard_failures:
        raise RuntimeError(
            f"{len(hard_failures)}/{len(scenes_to_generate)} scene generations failed with a non-safety "
            f"error (first: {hard_failures[0][1]}). Refusing to schedule partial/placeholder posts -- "
            f"check cloud.higgsfield.ai billing and the HIGGSFIELD_API_KEY_ID/SECRET secrets."
        )

    manifest_items = []
    offset = mux_audio.next_offset(state)
    for i, meta in enumerate(scenes_meta):
        scene = meta["scene"]
        result = results[i]
        err = errors[i]
        if result is None:
            print(f"[SAFETY] Scene '{scene['title']}' was flagged nsfw by Higgsfield -- skipping this post entirely today.")
            continue

        final_path = os.path.join(meta["out_dir"], "final.mp4")
        mux_audio.mux(result["video_path"], music_local_path, offset, final_path)
        # Step the offset forward for the NEXT scene in this same run too,
        # so 3 posts in one run don't all use the identical music slice.
        offset += mux_audio.CLIP_DURATION_SECONDS
        if offset + mux_audio.CLIP_DURATION_SECONDS >= mux_audio.TRACK_DURATION_SECONDS:
            offset = 0.0

        # remove the intermediate silent video + raw still so only the
        # final muxed clip gets committed to the repo
        for intermediate in (result["video_path"], result["still_path"]):
            if os.path.exists(intermediate):
                os.remove(intermediate)

        text = HASHTAGS if not CAPTION else f"{CAPTION}\n\n{HASHTAGS}"
        manifest_items.append({
            "title": scene["title"],
            "scene_index": meta["scene_index"],
            "text": text,
            "video_repo_path": os.path.relpath(final_path, REPO_ROOT),
            "scheduled_at": scheduled_times[i].strftime("%Y-%m-%dT%H:%M:%SZ"),
        })

    os.remove(music_local_path)

    if not manifest_items:
        raise RuntimeError("Every scene in this run was nsfw-blocked -- nothing to schedule. Check the scene bank prompts.")

    manifest = {
        "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "start_index": start_index,
        "count": count,
        "final_scene_index": scenes_meta[-1]["scene_index"],
        "final_scheduled_up_to": scheduled_times[len(manifest_items) - 1].strftime("%Y-%m-%dT%H:%M:%SZ"),
        "final_music_offset": offset,
        "items": manifest_items,
    }
    os.makedirs(os.path.dirname(manifest_path()), exist_ok=True)
    with open(manifest_path(), "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"[OK] Generated {len(manifest_items)} posts. Manifest written to {manifest_path()}")


def phase_schedule():
    state = load_state()
    with open(manifest_path()) as f:
        manifest = json.load(f)

    success_count = 0
    attempt_count = 0
    for item in manifest["items"]:
        video_url = raw_url(item["video_repo_path"])
        for channel_name in CHANNELS:
            attempt_count += 1
            try:
                buffer_client.create_video_post(
                    channel_name, item["text"], video_url, item["scheduled_at"], BUFFER_TOKEN_ENV
                )
                print(f"[OK] Scheduled '{item['title']}' to {channel_name} for {item['scheduled_at']}")
                success_count += 1
            except Exception as e:
                print(f"[ERROR] Failed to schedule '{item['title']}' to {channel_name}: {e}")

    print(f"[SUMMARY] {success_count}/{attempt_count} posts scheduled successfully.")

    if success_count == 0:
        raise RuntimeError(
            f"All {attempt_count} Buffer post attempts failed -- NOT advancing state "
            f"(last_scene_index/scheduled_up_to/music_offset unchanged). See [ERROR] lines above."
        )

    state["last_scene_index"] = manifest["final_scene_index"]
    state["scheduled_up_to"] = manifest["final_scheduled_up_to"]
    state["music_offset_seconds"] = manifest["final_music_offset"]
    state["last_run_at"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    state["last_run_slot"] = "github_actions_autonomous_bot"
    save_state(state)

    os.remove(manifest_path())


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("generate", "schedule"):
        print("Usage: python main.py <generate|schedule>")
        sys.exit(1)
    (phase_generate if sys.argv[1] == "generate" else phase_schedule)()
