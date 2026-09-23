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

Rewritten with specific, named architectural and environmental detail in
each scene (particular carvings, banners, wear, wildlife, weather) so
every image reads as a distinct, thought-out place rather than a
generic "castle/moor/forest" template.
"""

SCENES = [
    {
        "title": "grand staircase",
        "has_people": True,
        "still_prompt": (
            "Wide establishing shot: a lone hooded traveler climbing an "
            "immense spiral stone staircase carved into a ruined gothic "
            "castle tower, worn stone steps cracked and missing chunks at "
            "the outer edge, a collapsed section of banister opening onto "
            "empty air, seen from below as a small silhouette against the "
            "vast structure. Ravens perched in a shattered archway above. "
            "Moonlight and drifting fog, torchlight flickering in distant "
            "windows, a faded heraldic banner hanging in tatters from a "
            "rampart. Painterly, cinematic, hyper-detailed, visually "
            "stunning concept art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: fog "
            "drifting through the stairwell, torch flames flickering in the "
            "windows, the tattered banner rippling faintly, moonlight "
            "shifting through clouds. Epic, majestic dark fantasy mood, not "
            "horror. No people appear or move into frame that weren't in "
            "the still, no text, no camera movement whatsoever."
        ),
    },
    {
        "title": "frozen lake ruins",
        "has_people": False,
        "still_prompt": (
            "Wide establishing shot: the shattered remains of a stone "
            "bridge crossing a vast frozen lake at dusk, one collapsed "
            "arch jutting from the ice at a broken angle, jagged frost "
            "patterns spreading across the surface, dead trees with "
            "frost-rimed branches framing the scene, a colossal ruined "
            "citadel with one crumbling spire looming on the far shore, "
            "a single set of old wolf tracks crossing the ice. No people. "
            "Painterly, cinematic, hyper-detailed, visually stunning "
            "concept art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: mist "
            "drifting low across the ice, snow falling gently, distant "
            "clouds shifting behind the citadel. Epic, majestic dark "
            "fantasy mood, not horror. No people appear or move into frame, "
            "no text, no camera movement whatsoever."
        ),
    },
    {
        "title": "rope bridge crossing",
        "has_people": True,
        "still_prompt": (
            "Wide establishing shot: a line of six small hooded travelers "
            "crossing a long, sagging rope bridge strung between two "
            "cliffs over a misty chasm, one plank visibly missing near the "
            "middle of the span, a pack mule led at the rear of the line, "
            "seen from a distance as tiny figures dwarfed by the "
            "landscape. Dramatic stormlight breaking through heavy clouds, "
            "a hawk circling far below. Painterly, cinematic, "
            "hyper-detailed, visually stunning concept art, vertical "
            "composition, no text."
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
            "Wide establishing shot: a colossal dragon with weathered, "
            "battle-scarred scales perched atop a ruined watchtower "
            "silhouetted against an enormous blood-red moon, wings half "
            "spread revealing torn membrane along one edge, a scattering "
            "of broken siege equipment abandoned at the tower's base, "
            "embers drifting through the night air from a smoldering fire "
            "below. No people. Painterly, cinematic, hyper-detailed, "
            "visually stunning concept art, vertical composition, no "
            "text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: embers "
            "drifting upward, smoke curling from the tower, the dragon's "
            "wings shifting slightly, clouds crossing the blood moon. "
            "Epic, majestic dark fantasy mood, not horror. No people "
            "appear, no text, no camera movement whatsoever."
        ),
    },
    {
        "title": "misty moor procession",
        "has_people": True,
        "still_prompt": (
            "Wide establishing shot: a distant caravan of cloaked figures "
            "and torches moving across an endless misty moor at twilight, "
            "tiny against the vast open landscape, a creaking wooden cart "
            "with one wheel bound in rope trailing behind them, a ring of "
            "ancient lichen-covered standing stones nearby with strange "
            "carved symbols worn nearly smooth by weather. Painterly, "
            "cinematic, hyper-detailed, visually stunning concept art, "
            "vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: mist "
            "rolling across the moor, torch flames flickering, grass "
            "swaying faintly in the wind. Epic, majestic dark fantasy "
            "mood, not horror. No new people appear that weren't in the "
            "still, no text, no camera movement whatsoever."
        ),
    },
    {
        "title": "sunken cathedral",
        "has_people": False,
        "still_prompt": (
            "Wide establishing shot: a vast gothic cathedral half sunken "
            "into a black swamp, its rose window shattered into jagged "
            "shards still clinging to the tracery, spires leaning at "
            "different angles and covered in thick vines, a single broken "
            "bell visible through a collapsed section of roof, pale "
            "moonlight breaking through storm clouds above, herons wading "
            "at the cathedral's flooded threshold. No people. Painterly, "
            "cinematic, hyper-detailed, visually stunning concept art, "
            "vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: mist "
            "rising off the swamp water, clouds drifting past the moon, "
            "vines swaying faintly. Epic, majestic dark fantasy mood, not "
            "horror. No people appear, no text, no camera movement "
            "whatsoever."
        ),
    },
    {
        "title": "cliffside watcher",
        "has_people": True,
        "still_prompt": (
            "Wide establishing shot: a single armored knight in a dented "
            "breastplate standing at the edge of a towering cliff, a "
            "notched sword planted point-down in the rock beside him, "
            "small against an immense view of jagged mountains and a "
            "distant storm, cloak billowing, a worn banner staff strapped "
            "across his back with the cloth long since torn away. "
            "Painterly, cinematic, hyper-detailed, visually stunning "
            "concept art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: the "
            "knight's cloak rippling in the wind, storm clouds rolling in "
            "the distance, mist drifting along the cliff edge. Epic, "
            "majestic dark fantasy mood, not horror. No new people appear, "
            "no text, no camera movement whatsoever."
        ),
    },
    {
        "title": "burning watchtower",
        "has_people": False,
        "still_prompt": (
            "Wide establishing shot: an ancient stone watchtower on a "
            "rocky hilltop with a single beacon fire burning at its peak "
            "inside a cracked iron brazier, one section of the parapet "
            "collapsed into rubble at the base, silhouetted against a vast "
            "starry night sky and distant mountain range, an owl perched "
            "on the tower's flagpole where no flag remains. No people. "
            "Painterly, cinematic, hyper-detailed, visually stunning "
            "concept art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: the "
            "beacon fire flickering and casting shifting light, smoke "
            "drifting upward, stars twinkling faintly. Epic, majestic dark "
            "fantasy mood, not horror. No people appear, no text, no "
            "camera movement whatsoever."
        ),
    },
    {
        "title": "the wild hunt",
        "has_people": True,
        "still_prompt": (
            "Wide establishing shot: a ghostly procession of hooded riders "
            "on antlered steeds and pale hounds with glowing eyes crossing "
            "the night sky above a vast dark forest, small and distant "
            "against the huge composition, a lone stag fleeing through the "
            "treeline below them, pale moonlight outlining the riders' "
            "trailing cloaks. Painterly, cinematic, hyper-detailed, "
            "visually stunning concept art, vertical composition, no "
            "text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: clouds "
            "drifting past the moon, faint mist over the forest canopy, "
            "the riders' cloaks rippling. Epic, majestic dark fantasy "
            "mood, not horror. No new people appear, no text, no camera "
            "movement whatsoever."
        ),
    },
    {
        "title": "the green man grove",
        "has_people": False,
        "still_prompt": (
            "Wide establishing shot: an enormous ancient tree carved with "
            "a leaf-covered face, moss thick in the grooves of its bark and "
            "one eye socket hollowed into a small nesting hole, standing "
            "alone in a vast misty grove of dead and living trees, small "
            "offerings of ribbon and carved trinkets tied to its lowest "
            "branches, pale light filtering through the canopy. No people. "
            "Painterly, cinematic, hyper-detailed, visually stunning "
            "concept art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: mist "
            "drifting between the trees, leaves rustling faintly, the tied "
            "ribbons stirring, light shifting through the canopy. Epic, "
            "majestic dark fantasy mood, not horror. No people appear, no "
            "text, no camera movement whatsoever."
        ),
    },
    {
        "title": "baba yaga's hut",
        "has_people": True,
        "still_prompt": (
            "Wide establishing shot: a strange hut on giant chicken legs, "
            "wood shingles patched unevenly and a crooked chimney trailing "
            "smoke, standing deep in a vast dark forest clearing, a small "
            "distant figure approaching cautiously with a bundle held "
            "close, a bone fence glowing faintly around it with a single "
            "gate hanging open on one hinge. Painterly, cinematic, "
            "hyper-detailed, visually stunning concept art, vertical "
            "composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: mist "
            "curling around the hut's legs, the bone fence glowing and "
            "flickering faintly, smoke drifting from the chimney, trees "
            "swaying gently. Epic, majestic dark fantasy mood, not horror. "
            "No new people appear, no text, no camera movement whatsoever."
        ),
    },
    {
        "title": "castle in the clouds",
        "has_people": False,
        "still_prompt": (
            "Wide establishing shot: a vast gothic castle perched on a "
            "floating rock formation above an endless sea of clouds at "
            "sunset, one tower visibly leaning with scaffolding of old "
            "timber braced against its base, tattered banners in faded "
            "heraldic colors rippling from the walls, dramatic golden and "
            "purple light, a flock of dark birds wheeling around the "
            "highest spire. No people. Painterly, cinematic, "
            "hyper-detailed, visually stunning concept art, vertical "
            "composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with the camera completely locked in "
            "place, not moving at all. Only the scene itself moves: clouds "
            "drifting slowly below the castle, banners rippling on the "
            "towers, the birds wheeling around the spire, light shifting "
            "with the sunset. Epic, majestic dark fantasy mood, not "
            "horror. No people appear, no text, no camera movement "
            "whatsoever."
        ),
    },
]
