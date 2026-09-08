"""
Rotation bank of dark-fantasy scenes for the @ai_facts4u page's aesthetic
video pipeline. Each entry produces exactly ONE post: one still image
(Nano Banana Pro / Higgsfield Soul) animated into an 8s silent video
(Bytedance Seedance v1 Lite, camera_fixed=True), with the page's music
track muxed on afterward.

Rules locked in content-engine/niches/DARK_FANTASY_VIDEO_STYLE.md (read
that file before adding scenes):
  - Wide epic scale, NOT close-up portraits. A small subject (or nobody)
    against a vast dramatic environment.
  - People in roughly HALF of scenes only, always small/distant figures
    for scale, never the visual focus.
  - Medieval gothic / epic dark fantasy tone, not horror or gore.
  - Animate prompt always locks the camera completely still -- only
    ambient elements (clouds, mist, fire, fabric, embers) move.

`has_people` alternates true/false across the bank below by design so
consecutive posts don't repeat the same subject pattern.
"""

SCENES = [
    {
        "title": "grand staircase",
        "has_people": True,
        "still_prompt": (
            "Wide establishing shot: a lone hooded traveler climbing an immense "
            "spiral stone staircase carved into a ruined gothic castle tower, "
            "seen from below as a small silhouette against the vast structure. "
            "Moonlight and drifting fog, torchlight flickering in distant "
            "windows. Painterly, cinematic, hyper-detailed, visually stunning "
            "concept art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: fog "
            "drifting through the stairwell, torch flames flickering in the "
            "windows, moonlight shifting faintly through clouds. Epic, "
            "majestic dark fantasy mood, not horror. No people appear or move "
            "into frame that weren't in the still, no text, no camera "
            "movement whatsoever."
        ),
    },
    {
        "title": "frozen lake ruins",
        "has_people": False,
        "still_prompt": (
            "Wide establishing shot: the shattered remains of a stone bridge "
            "crossing a vast frozen lake at dusk, jagged ice and dead trees "
            "framing the scene, a colossal ruined citadel looming on the far "
            "shore. No people. Painterly, cinematic, hyper-detailed, visually "
            "stunning concept art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: mist "
            "drifting low across the ice, snow falling gently, distant clouds "
            "shifting behind the citadel. Epic, majestic dark fantasy mood, "
            "not horror. No people appear or move into frame, no text, no "
            "camera movement whatsoever."
        ),
    },
    {
        "title": "rope bridge crossing",
        "has_people": True,
        "still_prompt": (
            "Wide establishing shot: a line of small hooded travelers crossing "
            "a long rope bridge strung between two cliffs over a misty chasm, "
            "seen from a distance as tiny figures dwarfed by the landscape. "
            "Dramatic stormlight breaking through clouds. Painterly, "
            "cinematic, hyper-detailed, visually stunning concept art, "
            "vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: mist "
            "rolling through the chasm, the rope bridge swaying gently, "
            "clouds drifting and stormlight shifting. Epic, majestic dark "
            "fantasy mood, not horror. No new people appear or move into "
            "frame that weren't in the still, no text, no camera movement "
            "whatsoever."
        ),
    },
    {
        "title": "dragon and blood moon",
        "has_people": False,
        "still_prompt": (
            "Wide establishing shot: a colossal dragon perched atop a ruined "
            "watchtower silhouetted against an enormous blood-red moon, wings "
            "half spread, embers drifting through the night air. No people. "
            "Painterly, cinematic, hyper-detailed, visually stunning concept "
            "art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: embers "
            "drifting upward, smoke curling from the tower, the dragon's "
            "wings shifting slightly, clouds crossing the blood moon. Epic, "
            "majestic dark fantasy mood, not horror. No people appear, no "
            "text, no camera movement whatsoever."
        ),
    },
    {
        "title": "misty moor procession",
        "has_people": True,
        "still_prompt": (
            "Wide establishing shot: a distant caravan of cloaked figures and "
            "torches moving across an endless misty moor at twilight, tiny "
            "against the vast open landscape, a ring of ancient standing "
            "stones nearby. Painterly, cinematic, hyper-detailed, visually "
            "stunning concept art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: mist "
            "rolling across the moor, torch flames flickering, grass swaying "
            "faintly in the wind. Epic, majestic dark fantasy mood, not "
            "horror. No new people appear that weren't in the still, no "
            "text, no camera movement whatsoever."
        ),
    },
    {
        "title": "sunken cathedral",
        "has_people": False,
        "still_prompt": (
            "Wide establishing shot: a vast gothic cathedral half sunken into "
            "a black swamp, its spires leaning and covered in vines, pale "
            "moonlight breaking through storm clouds above. No people. "
            "Painterly, cinematic, hyper-detailed, visually stunning concept "
            "art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: mist "
            "rising off the swamp water, clouds drifting past the moon, vines "
            "swaying faintly. Epic, majestic dark fantasy mood, not horror. "
            "No people appear, no text, no camera movement whatsoever."
        ),
    },
    {
        "title": "cliffside watcher",
        "has_people": True,
        "still_prompt": (
            "Wide establishing shot: a single armored knight standing at the "
            "edge of a towering cliff, small against an immense view of "
            "jagged mountains and a distant storm, cloak billowing. Painterly, "
            "cinematic, hyper-detailed, visually stunning concept art, "
            "vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: the "
            "knight's cloak rippling in the wind, storm clouds rolling in the "
            "distance, mist drifting along the cliff edge. Epic, majestic "
            "dark fantasy mood, not horror. No new people appear, no text, no "
            "camera movement whatsoever."
        ),
    },
    {
        "title": "burning watchtower",
        "has_people": False,
        "still_prompt": (
            "Wide establishing shot: an ancient stone watchtower on a rocky "
            "hilltop with a single beacon fire burning at its peak, silhouetted "
            "against a vast starry night sky and distant mountain range. No "
            "people. Painterly, cinematic, hyper-detailed, visually stunning "
            "concept art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: the "
            "beacon fire flickering and casting shifting light, smoke drifting "
            "upward, stars twinkling faintly. Epic, majestic dark fantasy "
            "mood, not horror. No people appear, no text, no camera movement "
            "whatsoever."
        ),
    },
    {
        "title": "the wild hunt",
        "has_people": True,
        "still_prompt": (
            "Wide establishing shot: a ghostly procession of hooded riders and "
            "hounds crossing the night sky above a vast dark forest, small and "
            "distant against the huge composition, pale moonlight outlining "
            "them. Painterly, cinematic, hyper-detailed, visually stunning "
            "concept art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: clouds "
            "drifting past the moon, faint mist over the forest canopy, the "
            "riders' cloaks rippling. Epic, majestic dark fantasy mood, not "
            "horror. No new people appear, no text, no camera movement "
            "whatsoever."
        ),
    },
    {
        "title": "the green man grove",
        "has_people": False,
        "still_prompt": (
            "Wide establishing shot: an enormous ancient tree carved with a "
            "leaf-covered face, standing alone in a vast misty grove of dead "
            "and living trees, pale light filtering through the canopy. No "
            "people. Painterly, cinematic, hyper-detailed, visually stunning "
            "concept art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: mist "
            "drifting between the trees, leaves rustling faintly, light "
            "shifting through the canopy. Epic, majestic dark fantasy mood, "
            "not horror. No people appear, no text, no camera movement "
            "whatsoever."
        ),
    },
    {
        "title": "baba yaga's hut",
        "has_people": True,
        "still_prompt": (
            "Wide establishing shot: a strange hut on giant chicken legs "
            "standing deep in a vast dark forest clearing, a small distant "
            "figure approaching cautiously, a bone fence glowing faintly "
            "around it. Painterly, cinematic, hyper-detailed, visually "
            "stunning concept art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: mist "
            "curling around the hut's legs, the bone fence glowing and "
            "flickering faintly, trees swaying gently. Epic, majestic dark "
            "fantasy mood, not horror. No new people appear, no text, no "
            "camera movement whatsoever."
        ),
    },
    {
        "title": "castle in the clouds",
        "has_people": False,
        "still_prompt": (
            "Wide establishing shot: a vast gothic castle perched on a "
            "floating rock formation above an endless sea of clouds at "
            "sunset, dramatic golden and purple light. No people. Painterly, "
            "cinematic, hyper-detailed, visually stunning concept art, "
            "vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: clouds "
            "drifting slowly below the castle, banners rippling on the "
            "towers, light shifting with the sunset. Epic, majestic dark "
            "fantasy mood, not horror. No people appear, no text, no camera "
            "movement whatsoever."
        ),
    },
]
