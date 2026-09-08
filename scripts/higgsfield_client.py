"""
Thin client for Higgsfield's developer REST API (platform.higgsfield.ai),
used instead of the MCP connector because this runs headlessly in GitHub
Actions with no Claude session attached.

Adapted from workoutnow768-eng/auto-post7's higgsfield_client.py -- same
auth, same async submit/poll lifecycle, same "never use an nsfw result"
safety rule -- but this pipeline needs TWO model calls per post instead of
one:

  1. generate_image()        -- Soul v2 standard, produces the still.
  2. generate_video_from_image() -- Minimax Hailuo 2.3 standard
     image-to-video, animates that still into a silent clip with the
     camera locked (via prompt wording only -- see below). This model has
     no audio input/output at all, which is exactly what this page needs
     (music gets muxed on separately in mux_audio.py).

     image_url is fed the Higgsfield-hosted URL returned by the still-image
     step directly (Higgsfield keeps generation outputs available for at
     least 7 days per their docs) -- no separate re-upload step needed.

     FIX 2026-09-08 (round 3): originally targeted Bytedance Seedance v1
     Lite (POST /bytedance/seedance/v1/lite/image-to-video on
     api.higgsfield.ai), which is a real, correctly-documented endpoint --
     but 404'd with model_not_found on every host/path variant tried.
     Root cause found via the cloud.higgsfield.ai dashboard: this account's
     developer API key has ONLY 3 models enabled at all -- Soul 2, Soul
     Cinema, Soul ID -- all image models, zero video, regardless of plan
     tier (confirmed on a near-top-tier plan). This is a different, more
     limited catalog than the Higgsfield MCP/app account (which does have
     Seedance 2.0 Mini -- that's what generated the manual test clips
     earlier in this project).

     Switched to Minimax Hailuo 2.3 (POST
     /minimax/hailuo-2.3/standard/image-to-video on api.higgsfield.ai) as
     the first model outside the 3 confirmed-enabled ones to actually try
     -- a different vendor than Bytedance, so it isn't necessarily gated by
     the same enablement. Its request shape is simpler/different: no
     resolution or camera_fixed params at all (schema per Higgsfield's
     public openapi.json: prompt, image_url, duration [6 or 10 only],
     prompt_optimizer). Camera-lock now relies entirely on the prompt
     wording (already explicit about it in scene_bank.py's animate_prompt
     text) since there's no structured param for it on this model.
     duration=6 (not 8) because 6/10 are the only allowed values -- 6 is
     the cheaper of the two. mux_audio.CLIP_DURATION_SECONDS was updated
     to match.

     If this also turns out to be unavailable (404 model_not_found), that
     confirms the account's developer API key just has no video access at
     all yet, independent of vendor -- at that point the fix is on
     Higgsfield's side (enable a video model for this key), not more
     endpoint-guessing here.
"""
import os
import time
import requests
import concurrent.futures

IMAGE_BASE_URL = "https://platform.higgsfield.ai"
GENERATE_IMAGE_ENDPOINT = f"{IMAGE_BASE_URL}/higgsfield-ai/soul/v2/standard"
GENERATE_VIDEO_ENDPOINT = "https://api.higgsfield.ai/minimax/hailuo-2.3/standard/image-to-video"

POLL_INTERVAL_SECONDS = 5
POLL_TIMEOUT_SECONDS = 300  # video jobs run longer than image jobs


class GenerationBlocked(Exception):
    """Raised when Higgsfield flags a generation as nsfw -- never use the result."""


class GenerationFailed(Exception):
    pass


def _auth_header():
    key_id = os.environ["HIGGSFIELD_API_KEY_ID"]
    key_secret = os.environ["HIGGSFIELD_API_KEY_SECRET"]
    return {"Authorization": f"Key {key_id}:{key_secret}"}


def _submit(endpoint, payload):
    resp = requests.post(
        endpoint,
        headers={**_auth_header(), "Content-Type": "application/json", "Accept": "application/json"},
        json=payload,
        timeout=30,
    )
    if not resp.ok:
        raise GenerationFailed(f"HTTP {resp.status_code} from Higgsfield ({endpoint}): {resp.text[:500]}")
    data = resp.json()
    status_url = data.get("status_url")
    if not status_url:
        raise GenerationFailed(f"No status_url in response: {data}")
    return status_url


def poll_until_done(status_url, poll_interval=POLL_INTERVAL_SECONDS, timeout=POLL_TIMEOUT_SECONDS):
    """Polls status_url until a terminal state. Returns the final JSON payload."""
    elapsed = 0
    while elapsed < timeout:
        resp = requests.get(status_url, headers=_auth_header(), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status")
        if status == "completed":
            return data
        if status == "nsfw":
            raise GenerationBlocked(f"Higgsfield flagged this generation as nsfw: {data}")
        if status in ("failed", "canceled"):
            raise GenerationFailed(f"Generation ended in status={status}: {data}")
        time.sleep(poll_interval)
        elapsed += poll_interval
    raise GenerationFailed(f"Timed out after {timeout}s waiting on {status_url}")


def _first_url_in(result, *candidate_keys):
    """Extraction is defensive on purpose: the public OpenAPI spec documents
    request shapes but not the exact completed-job response shape for every
    model, and the image endpoint's own convention (images: [{url}]) may
    not carry over 1:1 to video. Tries several plausible key names/shapes
    rather than hard-failing on one guess."""
    for key in candidate_keys:
        val = result.get(key)
        if isinstance(val, list) and val:
            item = val[0]
            if isinstance(item, dict) and item.get("url"):
                return item["url"]
            if isinstance(item, str):
                return item
        if isinstance(val, dict) and val.get("url"):
            return val["url"]
        if isinstance(val, str):
            return val
    return None


def download_file(url, out_path):
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(resp.content)
    return out_path


def generate_image(prompt, out_path, aspect_ratio="9:16", resolution="1080p", max_retries=2):
    """
    End-to-end still generation: submit -> poll -> download. Returns
    (local_path, hosted_url) -- the hosted_url is fed straight into
    generate_video_from_image() so the video model can fetch the same
    image without a re-upload round trip.

    FIX 2026-09-08: this originally defaulted to resolution="2k" (the
    value the Higgsfield MCP tool's alias accepts), but the raw
    platform.higgsfield.ai REST API used here rejects that outright --
    confirmed via a live GitHub Actions run failing 3/3 scenes with
    "HTTP 422 ... Input should be '720p' or '1080p'". The Soul v2
    standard endpoint's resolution enum on this API is only 720p/1080p,
    no "2k"/"4k" aliases -- use "1080p" for the highest quality still
    this endpoint actually supports.
    """
    last_err = None
    for attempt in range(max_retries):
        try:
            status_url = _submit(GENERATE_IMAGE_ENDPOINT, {
                "prompt": prompt, "aspect_ratio": aspect_ratio, "resolution": resolution,
            })
            result = poll_until_done(status_url)
            image_url = _first_url_in(result, "images", "image", "outputs")
            if not image_url:
                raise GenerationFailed(f"Completed but no image url in payload: {result}")
            download_file(image_url, out_path)
            return out_path, image_url
        except GenerationBlocked:
            raise  # never swallow/retry an nsfw block silently
        except (GenerationFailed, requests.RequestException) as e:
            last_err = e
            time.sleep(3)
    raise GenerationFailed(f"Failed after {max_retries} attempts: {last_err}")


def generate_video_from_image(prompt, image_url, out_path, duration=6, max_retries=2):
    """
    End-to-end animate step: submit -> poll -> download the silent video.
    Minimax Hailuo 2.3 has no camera_fixed param -- the "camera completely
    locked, only ambient elements move" instruction lives entirely in the
    prompt text (see scene_bank.py's animate_prompt wording). duration
    must be 6 or 10 -- 6 is the cheaper option and what this pipeline
    always uses. prompt_optimizer=False keeps the prompt literal instead
    of letting Higgsfield rewrite it, since these prompts are already
    deliberately worded to enforce the style lock.
    """
    last_err = None
    for attempt in range(max_retries):
        try:
            status_url = _submit(GENERATE_VIDEO_ENDPOINT, {
                "prompt": prompt,
                "image_url": image_url,
                "duration": duration,
                "prompt_optimizer": False,
            })
            result = poll_until_done(status_url)
            video_url = _first_url_in(result, "videos", "video", "outputs")
            if not video_url:
                raise GenerationFailed(f"Completed but no video url in payload: {result}")
            download_file(video_url, out_path)
            return out_path
        except GenerationBlocked:
            raise
        except (GenerationFailed, requests.RequestException) as e:
            last_err = e
            time.sleep(3)
    raise GenerationFailed(f"Failed after {max_retries} attempts: {last_err}")


def generate_post_concurrent(scene, out_dir, max_workers=3):
    """
    Not used for the batch step (video jobs must run AFTER their still
    completes, so scenes are still generated one at a time end-to-end --
    see main.py). Kept here as the single place that knows the full
    still->video pipeline for one scene, so main.py can run several
    scenes' still+video pairs concurrently via a thread pool without
    duplicating this logic.
    """
    raise NotImplementedError("call generate_one_post(scene, out_dir) per scene instead")


def generate_one_post(scene, out_dir):
    """
    Runs the full still -> video pipeline for one scene dict (see
    scene_bank.py). Returns {"still_path":, "video_path":}. Raises
    GenerationBlocked/GenerationFailed same as the underlying calls --
    caller decides whether to skip or abort the whole run.
    """
    still_path = os.path.join(out_dir, "still.png")
    video_path = os.path.join(out_dir, "video_silent.mp4")

    _, image_url = generate_image(scene["still_prompt"], still_path)
    generate_video_from_image(scene["animate_prompt"], image_url, video_path)

    return {"still_path": still_path, "video_path": video_path}


def generate_posts_concurrent(scenes, out_dirs, max_workers=3):
    """
    scenes: list of scene dicts. out_dirs: parallel list of output dirs.
    Runs generate_one_post for each scene concurrently (I/O-bound HTTP
    calls, same reasoning as auto-post7's generate_images_concurrent).
    max_workers=3 (lower than the image-only pipeline's 5) since each job
    here is two sequential Higgsfield calls (image then video) instead of
    one, so each thread holds a slot roughly twice as long.

    Returns (results, errors), both lists parallel to scenes. results[i]
    is {"still_path":, "video_path":} on success, None on failure.
    errors[i] is None on success, or the exception instance on failure.
    """
    results = [None] * len(scenes)
    errors = [None] * len(scenes)

    def _run_one(index, scene, out_dir):
        try:
            return index, generate_one_post(scene, out_dir), None
        except (GenerationBlocked, GenerationFailed) as e:
            return index, None, e

    if not scenes:
        return results, errors

    with concurrent.futures.ThreadPoolExecutor(max_workers=min(max_workers, len(scenes))) as pool:
        futures = [pool.submit(_run_one, i, scenes[i], out_dirs[i]) for i in range(len(scenes))]
        for future in concurrent.futures.as_completed(futures):
            index, result, err = future.result()
            results[index] = result
            errors[index] = err

    return results, errors
