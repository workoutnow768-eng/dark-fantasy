"""
Muxes the page's music track onto a silent generated video with ffmpeg.
This is the exact pattern already proven manually in this session (via
Higgsfield's sandbox_exec) for the first 3 test posts -- copies the video
stream untouched, re-encodes only the audio to AAC, and fades in/out so
consecutive posts using the same long track don't have a hard cut.

Requires the `ffmpeg` binary on PATH (installed via apt in the workflow).
"""
import os
import json
import subprocess

TRACK_DURATION_SECONDS = 254.088  # "Creaking Hallways.mp3" -- see state file for rotation offset
CLIP_DURATION_SECONDS = 8.042      # matches the ~8s Seedance output; ffmpeg -t trims to this exactly
FADE_SECONDS = 0.5


def mux(video_path, audio_path, offset_seconds, out_path):
    """
    Cuts an 8s window out of audio_path starting at offset_seconds, fades
    it in/out, and muxes it onto video_path (video stream copied, not
    re-encoded). Raises subprocess.CalledProcessError on ffmpeg failure --
    caller should treat that as a hard failure, not silently post a
    silent/broken video.
    """
    fade_out_start = CLIP_DURATION_SECONDS - FADE_SECONDS
    filter_complex = (
        f"[1:a]afade=t=in:st=0:d={FADE_SECONDS},"
        f"afade=t=out:st={fade_out_start}:d={FADE_SECONDS}[a]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-ss", str(offset_seconds), "-t", str(CLIP_DURATION_SECONDS), "-i", audio_path,
        "-filter_complex", filter_complex,
        "-map", "0:v", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        out_path,
    ]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return out_path


def next_offset(state):
    """
    Steps the music offset forward by one clip length each run so
    consecutive posts don't reuse the exact same slice of the track, and
    wraps back to 0 once the track runs out. State-tracked in
    state["music_offset_seconds"] so this survives across workflow runs.
    """
    offset = state.get("music_offset_seconds", 0.0)
    if offset + CLIP_DURATION_SECONDS >= TRACK_DURATION_SECONDS:
        offset = 0.0
    return offset
