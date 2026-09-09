# dark-fantasy

Fully autonomous daily video pipeline for the @ai_facts4u ("Food_for_u")
TikTok page's pivot to pure dark-fantasy aesthetic content. Runs on GitHub
Actions -- once the secrets below are set, this posts itself every day
with no further manual steps.

Sister repo to [workoutnow768-eng/auto-post7](https://github.com/workoutnow768-eng/auto-post7)
(the fitness/recipe image-carousel bot) -- same architecture (Higgsfield
REST API -> render/process locally -> commit to repo -> Buffer GraphQL API
-> schedule), but this pipeline generates actual VIDEO (still image
animated into an 8s clip, camera locked static) instead of image
carousels, and muxes the page's own music track on with ffmpeg before
posting. See `content-engine/niches/DARK_FANTASY_VIDEO_STYLE.md` in the
main content-engine repo for the full style lock this pipeline follows.

## What one run does

1. **Generate** (`scripts/main.py generate`): picks the next 3 scenes from
   `scripts/scene_bank.py`'s rotation, for each one:
   - generates a still image (Higgsfield Soul v2, 1080p, 9:16)
   - animates it into a 6s silent video (Minimax Hailuo 2.3 -- Bytedance
     Seedance was the original plan but this account's developer API key
     has no video models enabled for it, only Minimax; camera lock is
     enforced via prompt wording only, since this model has no structured
     camera-lock parameter)
   - mixes in the page's music track (`ffmpeg`, fading in/out, stepping
     through the track so consecutive posts don't reuse the same slice)
   - writes a manifest of the 3 finished .mp4 paths + scheduled times
2. **Commit + push** those .mp4 files (Buffer needs a public URL to fetch
   from, which only exists once they're live on GitHub).
3. **Schedule** (`scripts/main.py schedule`): reads the manifest, creates
   one Buffer post per video per channel (TikTok, Instagram, YouTube),
   then updates the rotation state and removes the manifest.

Runs daily at 17:17 UTC via the scheduled workflow, or on demand from the
Actions tab (**Run workflow** button).

## One-time setup

### 1. Make this repo public

**Required.** Buffer fetches video files from `raw.githubusercontent.com`,
which only serves unauthenticated requests on public repos. This repo is
currently **private** -- go to **Settings → General → Danger Zone → Change
repository visibility → Make public** before the first scheduled run, or
every post will fail with a "could not fetch media" error from Buffer.

### 2. Add repo secrets

Go to **Settings → Secrets and variables → Actions → New repository
secret** and add these four. I (Claude) never see or handle any of these
values -- you paste them directly into GitHub's own UI, same as the
existing auto-post7 setup:

| Secret | Where to get it |
|---|---|
| `HIGGSFIELD_API_KEY_ID` | [cloud.higgsfield.ai](https://cloud.higgsfield.ai) -- API keys section. **This is a separate credit pool from the Higgsfield app/MCP balance** -- confirmed the hard way in auto-post7's history. Check this account has its own credits before the bot's first run. |
| `HIGGSFIELD_API_KEY_SECRET` | Same page, paired with the key ID above. |
| `BUFFER_ACCESS_TOKEN_DARKFANTASY` | [publish.buffer.com/settings/api](https://publish.buffer.com/settings/api) on the **podcasterclips** Buffer account (same account as the recipe pipeline's `ai_facts4u`/`daily_ai_factz` channels). Use a **separate** token from `BUFFER_ACCESS_TOKEN_RECIPE` even though it's the same account -- keeps the two pipelines' credentials independent. |
| `MUSIC_TRACK_URL` | Public URL to "Creaking Hallways.mp3" -- already uploaded to Higgsfield's CDN this session, use that URL directly. |

### 3. Confirm the "Factual days" YouTube channel is connected

Unlike the recipe pipeline (which can't post to YouTube -- Buffer rejects
image-only posts there), this pipeline generates real video, so YouTube is
included in `scripts/main.py`'s `CHANNELS` list. Confirm the "Factual
days" channel is still connected in Buffer before the first run, or drop
it from `CHANNELS` if you'd rather add it back later.

### 4. Test with a manual run

Once secrets are set and the repo is public, go to the **Actions** tab →
**Daily Dark Fantasy Bot** → **Run workflow** to trigger one run
immediately rather than waiting for the next scheduled time. Watch the
run's logs for `[OK]`/`[ERROR]`/`[SAFETY]` lines -- the pipeline fails
loudly (red X) rather than silently posting broken content if generation
or scheduling has a systemic problem.

## Extending the scene bank

`scripts/scene_bank.py` has 12 scenes to start. The rotation wraps back to
the first scene once it runs through all of them (posts_per_day=3 means it
takes 4 days to cycle). Add more scenes any time by appending to `SCENES`
-- each needs `title`, `has_people` (keep it to roughly half the bank),
`still_prompt`, and `animate_prompt`. Follow the templates and rules in
`content-engine/niches/DARK_FANTASY_VIDEO_STYLE.md` exactly (wide epic
scale not portraits, camera always locked static, no on-screen text, no
horror/gore).

## Rotation state

`state/dark_fantasy_state.json` tracks which scene is next
(`last_scene_index`), the next open posting slot (`scheduled_up_to`), and
where in the music track the next mux should start
(`music_offset_seconds`). The bot owns these fields -- don't hand-edit them
while the scheduled workflow is active, same rule as auto-post7's state
files.

## Cost per run (confirmed 2026-09-09)

- Still (Soul v2, 1080p) + animate (Minimax Hailuo 2.3, 6s): ~5cr per post
  combined (measured via the "Credits Used" delta on
  cloud.higgsfield.ai/dashboard for one real post).
- At 3 posts/day: ~15cr/day against the `cloud.higgsfield.ai` API credit
  pool (not the Higgsfield app/MCP balance -- see the secrets table above).
