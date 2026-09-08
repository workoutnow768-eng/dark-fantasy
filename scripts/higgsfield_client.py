"""
Thin client for Higgsfield's developer REST API (platform.higgsfield.ai),
used instead of the MCP connector because this runs headlessly in GitHub
Actions with no Claude session attached.

Adapted from workoutnow768-eng/auto-post7's higgsfield_client.py -- same
auth, same async submit/poll lifecycle, same "never use an nsfw result"
safety rule -- but this pipeline needs TWO model calls per post instead of
one:

  1. generate_image()        -- Soul v2 standard, produces the still.
  2. generate_video_from_image() -- Bytedance Seedance v1 Lite
     image-to-video, animates that still into an 8s silent clip with the
     camera locked (camera_fixed=True). Confirmed against Higgsfield's
     public OpenAPI spec (docs.higgsfield.ai/docs/openapi.json) 2026-09-08:
     endpoint is POST /bytedance/seedance/v1/lite/image-to-video, body
     {prompt, image_url, duration (2-12s), resolution (480/720/1080),
     aspect_ratio, camera_fixed}. This model has no audio input/output at
     all -- there is no generate_audio flag to set because it never
     produces sound, which is exactly what this page needs (music gets
     muxed on separately in mux_audio.py).

     image_url is fed the Higgsfield-hosted URL returned by the still-image
     step directly (Higgsfield keeps generation outputs available for at
     least 7 days per their docs) -- no separate re-upload step needed.

     FIX 2026-09-08 (round 2): the endpoint path above is correct, but
     platform.higgsfield.ai (the host auto-post7 already uses successfully
     for images) 404s on it with {"detail":"model_not_found"} -- confirmed
     via a live Actions run where all 3 stills generated fine on that host
     but every video call 404'd. docs.higgsfield.ai's own quickstart curl
     example targets a DIFFERENT host, api.higgsfield.ai, which is what its
     public openapi.json (where this endpoint path came from) actually
     describes. platform.higgsfield.ai and api.higgsfield.ai apparently
     serve different model catalogs under the same auth. Image generation
     stays on platform.higgsfield.ai (proven working); video generation now
     targets api.higgsfield.ai instead.
"""
import os
import time
import requests
import concurrent.futures

IMAGE_BASE_URL = "https://platform.higgsfield.ai"
GENERATE_IMAGE_ENDPOINT = f"{IMAGE_BASE_URL}/higgsfield-ai/soul/v2/standard"

# Still uncertain which exact host/path combo this account's video model
# lives at (see the fix note above) -- tried in order, first one that
# doesn't 404 with "model_not_found" wins. A non-404 failure (bad prompt,
# auth, nsfw, etc) is a REAL error and is raised immediately without
# trying the rest of the list, so this never masks an actual problem.
GENERATE_VIDEO_ENDPOINT_CANDIDATES = [
    "https://api.higgsfield.ai/bytedance/seedance/v1/lite/image-to-video",
    "https://platform.higgsfield.ai/bytedance-ai/seedance/v1/lite/image-to-video",
    "https://platform.higgsfield.ai/bytedance/seedance/v1/lite/image-to-video",
]

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


_working_video_endpoint = None  # cached once one candidate succeeds, so later calls in the same run skip straight to it


def _submit_video(payload):
    """Tries each URL in GENERATE_VIDEO_ENDPOINT_CANDIDATES until one
    doesn't 404 with model_not_found. Caches the winner for the rest of
    this process. Raises the LAST candidate's error if every candidate
    404s, or immediately raises any non-404 error (that's a real failure,
    not a wrong-endpoint guess)."""
    global _working_video_endpoint
    candidates = [_working_video_endpoint] if _working_video_endpoint else GENERATE_VIDEO_ENDPOINT_CANDIDATES
    last_err = None
    for endpoint in candidates:
        try:
            result = _submit(endpoint, payload)
            _working_video_endpoint = endpoint
            return result
        except GenerationFailed as e:
            msg = str(e)
            if "404" in msg and "model_not_found" in msg:
                last_err = e
                continue
            raise  # a real error (bad request, auth, etc) -- don't hide it by trying other URLs
    raise GenerationFailed(f"No working video endpoint found among {candidates}. Last error: {last_err}")


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


def generate_video_from_image(prompt, image_url, out_path, duration=8, resolution="720",
                               aspect_ratio="9:16", max_retries=2):
    """
    End-to-end animate step: submit -> poll -> download the silent video.
    camera_fixed=True always -- this page's whole visual identity is a
    completely static camera with only the scene itself moving (see
    content-engine/niches/DARK_FANTASY_VIDEO_STYLE.md). Never pass
    camera_fixed=False here.
    """
    last_err = None
    for attempt in range(max_retries):
        try:
            status_url = _submit_video({
                "prompt": prompt,
                "image_url": image_url,
                "duration": duration,
                "resolution": resolution,
                "aspect_ratio": aspect_ratio,
                "camera_fixed": True,
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
