"""
Thin client for Buffer's public GraphQL API (api.buffer.com), adapted from
workoutnow768-eng/auto-post7's buffer_client.py for VIDEO posts instead of
image carousels.

Docs referenced: https://developers.buffer.com/guides/hosting-media.html
and https://developers.buffer.com/examples/create-video-post.html
(confirmed 2026-09-08) -- a video asset is `{"video": {"url": ...}}`,
same `assets` list shape as an image post but with exactly one entry
(one video per post here, not a carousel).

This pipeline reuses the podcasterclips Buffer account (same account the
food/recipe pipeline already uses for @ai_facts4u / TikTok and
daily_ai_factz / Instagram) -- per dez's explicit choice -- plus adds
YouTube, which the image-only recipe pipeline could never use (Buffer
rejects image-only posts to YouTube; this pipeline produces real video,
so that restriction doesn't apply here).

Needs its own repo secret: BUFFER_ACCESS_TOKEN_DARKFANTASY. Do NOT reuse
BUFFER_ACCESS_TOKEN_RECIPE even though it's the same underlying Buffer
account/org -- keeping one token per repo/pipeline avoids the exact
cross-pipeline credential mixup documented in auto-post7's README history.
"""
import os
import requests

API_URL = "https://api.buffer.com"


def _headers(token_env):
    token = os.environ[token_env]
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _graphql(query, token_env, variables=None):
    resp = requests.post(API_URL, headers=_headers(token_env), json={"query": query, "variables": variables or {}}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data and data["errors"]:
        raise RuntimeError(f"Buffer GraphQL error: {data['errors']}")
    return data["data"]


_ORGANIZATIONS_QUERY = """
query GetOrganizations {
  account {
    organizations {
      id
      name
    }
  }
}
"""

_CHANNELS_QUERY = """
query GetChannels($organizationId: OrganizationId!) {
  channels(input: { organizationId: $organizationId }) {
    id
    name
    displayName
    service
  }
}
"""

_org_id_cache = {}


def get_organization_id(token_env):
    if token_env in _org_id_cache:
        return _org_id_cache[token_env]
    data = _graphql(_ORGANIZATIONS_QUERY, token_env)
    orgs = (data.get("account") or {}).get("organizations") or []
    if not orgs:
        raise RuntimeError(f"No organizations found on the Buffer account for {token_env}.")
    _org_id_cache[token_env] = orgs[0]["id"]
    return _org_id_cache[token_env]


def list_channels(token_env):
    org_id = get_organization_id(token_env)
    data = _graphql(_CHANNELS_QUERY, token_env, {"organizationId": org_id})
    return data.get("channels", [])


_channel_cache = {}


def get_channel(channel_name, token_env):
    """Looks up a channel's full record by exact display name, matching
    against both `name` and `displayName` (see auto-post7's original for
    why -- some channel labels are custom displayNames, not handles)."""
    if token_env not in _channel_cache:
        by_label = {}
        for ch in list_channels(token_env):
            for label in (ch.get("name"), ch.get("displayName")):
                if label:
                    by_label[label] = ch
        _channel_cache[token_env] = by_label
    cache = _channel_cache[token_env]

    if channel_name in cache:
        return cache[channel_name]

    lowered = channel_name.strip().lower()
    matches = {name: ch for name, ch in cache.items() if name.strip().lower() == lowered}
    if len(matches) == 1:
        return next(iter(matches.values()))
    if not matches:
        raise RuntimeError(
            f"No Buffer channel found named '{channel_name}' on the account for {token_env}. "
            f"Available channels: {sorted(set(cache.keys()))}"
        )
    raise RuntimeError(f"Multiple channels matched '{channel_name}': {matches}")


# Instagram/Facebook video posts default to being read as Reels rather than
# plain feed posts -- using metadata type "reel" (rather than "post", which
# auto-post7 uses for its image carousels) for VIDEO assets on those two
# services. TikTok and YouTube need no such metadata block (matches
# auto-post7's confirmed behavior for TikTok; YouTube wasn't reachable from
# that image-only pipeline at all).
_VIDEO_METADATA_BY_SERVICE = {
    "instagram": lambda: {"instagram": {"type": "reel", "shouldShareToFeed": True}},
    "facebook": lambda: {"facebook": {"type": "reel"}},
}


def _video_metadata_for_service(service):
    builder = _VIDEO_METADATA_BY_SERVICE.get((service or "").lower())
    return builder() if builder else None


_CREATE_POST_MUTATION = """
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess {
      post { id text }
    }
    ... on MutationError {
      message
    }
  }
}
"""


def create_video_post(channel_name, text, video_url, scheduled_at_iso8601, token_env):
    """
    Schedules one video post to one channel. `video_url` must be a stable,
    publicly reachable URL (see hosting-media docs) -- this pipeline uses
    the muxed .mp4 committed to this repo's output/ dir and served via
    raw.githubusercontent.com, same pattern as auto-post7's images. That
    ONLY works if this repo is public (raw.githubusercontent.com 404s on
    private repos for unauthenticated requests) -- see README.
    """
    channel = get_channel(channel_name, token_env)
    post_input = {
        "text": text,
        "channelId": channel["id"],
        "schedulingType": "automatic",
        "mode": "customScheduled",
        "dueAt": scheduled_at_iso8601,
        "assets": [{"video": {"url": video_url}}],
    }
    metadata = _video_metadata_for_service(channel.get("service"))
    if metadata:
        post_input["metadata"] = metadata
    variables = {"input": post_input}
    result = _graphql(_CREATE_POST_MUTATION, token_env, variables)
    payload = result.get("createPost", {})
    if "message" in payload:
        raise RuntimeError(f"Buffer rejected the post for '{channel_name}': {payload['message']}")
    return payload.get("post")
