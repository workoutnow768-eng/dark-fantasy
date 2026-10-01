"""
Rotation bank of dark-fantasy scenes for the @ai_facts4u page's aesthetic
video pipeline. Each entry produces exactly ONE post: one still image
(Higgsfield Soul v2) animated into a 6s silent video (Minimax Hailuo 2.3
image-to-video), with the page's music track muxed on afterward.

Rules locked in content-engine/niches/DARK_FANTASY_VIDEO_STYLE.md (read
that file before adding scenes):
  - Wide epic scale, NOT close-up portraits. A small subject (or nobody)
    against a vast dramatic environment.
  - People in roughly HALF of scenes only, always small/distant figures
    for scale, never the visual focus.
  - Medieval gothic / epic dark fantasy tone, not horror or gore.

Third revision (2026-10-01), two changes based on direct feedback that
the videos "look like a still image with a tiny bit of flame movement"
and that the rotation "keeps almost repeating itself":

  1. Hailuo 2.3 (the video model this pipeline uses) has NO structural
     camera_fixed parameter -- camera behavior is driven entirely by the
     animate_prompt text. Every scene's animate_prompt previously said
     "camera completely locked... no camera movement whatsoever", which
     is a literal, direct instruction to the model to produce almost no
     motion. That was the actual cause of the "still image" complaint,
     not a model limitation -- it cost nothing to ask for movement
     instead, so every animate_prompt below now specifies a real,
     deliberate camera move (push-in, pull-back, pan, tilt, orbit, or
     dolly), a different one per scene so consecutive posts don't move
     the same way either.
  2. The bank grew from 12 to 18 scenes. At 3 posts/day the 12-scene
     bank fully repeated every 4 days, which is fast enough to notice --
     especially since every scene shared the same "wide shot, small
     figure, vast backdrop" composition. 18 scenes stretches one full
     cycle to 6 days and the 6 new scenes deliberately break from the
     "figure dwarfed by landscape" template (a close-in forge, a crowded
     feast hall, a collapsing tower interior) for more compositional
     variety within the cycle, not just more of the same shot repeated
     with different dressing.

`has_people` alternates true/false across the bank below by design so
consecutive posts don't repeat the same subject pattern.
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
            "Bring this image to life with a slow, smooth camera push-in "
            "toward the climbing traveler, gradually closing the distance "
            "over the full clip. Fog drifts through the stairwell, torch "
            "flames flicker in the windows, the tattered banner ripples, "
            "ravens shift on their perch. Epic, majestic dark fantasy "
            "mood, not horror. No new people appear, no text."
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
            "Bring this image to life with a slow camera pull-back, "
            "widening gradually from the broken bridge to reveal more of "
            "the frozen lake and the citadel beyond. Mist drifts low "
            "across the ice, snow falls gently, clouds shift behind the "
            "citadel. Epic, majestic dark fantasy mood, not horror. No "
            "people appear, no text."
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
            "Bri    {
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
            "Bring this image to life with a slow upward camera tilt, "
            "starting on the broken siege equipment at the tower's base "
            "and rising to reveal the full dragon against the blood moon. "
            "Embers drift upward, smoke curls from the tower, the "
            "dragon's wings shift and one wing flexes slightly, clouds "
            "cross the moon. Epic, majestic dark fantasy mood, not "
            "horror. No people appear, no text."
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
            "Bring this image to life with a slow diagonal camera drift, "
            "moving up and across toward the standing stones while the "
            "procession continues below. Mist rolls across the moor, "
            "torch flames flicker, the cart wheel creaks and turns, grass "
            "sways in the wind. Epic, majestic dark fantasy mood, not "
            "horror. No new people appear, no text."
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
            "Bring this image to life with a slow dolly forward, moving "
            "toward the cathedral's shattered rose window as if "
            "approaching across the swamp. Mist rises off the water, "
            "clouds drift past the moon, vines sway, a heron takes a slow "
            "step. Epic, majestic dark fantasy mood, not horror. No "
            "people appear, no text."
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
            "Bring this image to life with a slow pull-back and gentle "
            "downward tilt, widening from the knight to take in more of "
            "the mountain drop below him. His cloak ripples hard in the "
            "wind, storm clouds roll in the distance, mist drifts along "
            "the cliff edge. Epic, majestic dark fantasy mood, not "
            "horror. No new people appear, no text."
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
            "Bring this image to life with a slow push-in combined with a "
            "gentle pan toward the beacon fire at the tower's peak. The "
            "fire flickers and casts shifting light, smoke drifts upward, "
            "the owl ruffles its feathers once, stars twinkle faintly. "
            "Epic, majestic dark fantasy mood, not horror. No people "
            "appear, no text."
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
            "Bring this image to life with a slow rising camera movement, "
            "craning upward from the fleeing stag to follow the riders "
            "crossing the sky. Clouds drift past the moon, mist clings to "
            "the forest canopy, the riders' cloaks ripple, the hounds' "
            "legs stride. Epic, majestic dark fantasy mood, not horror. "
            "No new people appear, no text."
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
            "Bring this image to life with a slow orbital drift to the "
            "right around the great tree's face, revealing its profile "
            "gradually. Mist drifts between the trees, leaves rustle, the "
            "tied ribbons stir, light shifts through the canopy. Epic, "
            "majestic dark fantasy mood, not horror. No people appear, no "
            "text."
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
            "Bring this image to life with a slow push-in toward the hut, "
            "as the small figure continues its cautious approach. Mist "
            "curls around the hut's legs, which shift their weight "
            "slightly, the bone fence glows and flickers, smoke drifts "
            "from the chimney, trees sway. Epic, majestic dark fantasy "
            "mood, not horror. No new people appear, no text."
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
            "Bring this image to life with a slow pan left across the "
            "cloud sea toward the leaning tower. Clouds drift slowly "
            "below the castle, banners ripple hard on the towers, the "
            "birds wheel around the spire, light shifts with the sunset. "
            "Epic, majestic dark fantasy mood, not horror. No people "
            "appear, no text."
        ),
    },
    {
        "title": "the forge beneath the mountain",
        "has_people": True,
        "still_prompt": (
            "A vast underground forge hall carved into mountain rock, a "
            "single massive anvil at its center lit by the orange glow of "
            "a roaring furnace, a lone armored smith mid-swing with a "
            "hammer raised, sparks caught mid-shower around the strike "
            "point, chains of half-finished blades and shields hanging "
            "from the ceiling on iron hooks, steam rising from a quenching "
            "trough. Painterly, cinematic, hyper-detailed, visually "
            "stunning concept art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with a slow push-in on the anvil as "
            "the furnace light pulses and sparks shower from the strike "
            "point, steam curls from the quenching trough, the hanging "
            "chains sway slightly. Epic, majestic dark fantasy mood, not "
            "horror. No new people appear, no text."
        ),
    },
    {
        "title": "the long feast hall",
        "has_people": True,
        "still_prompt": (
            "The interior of a great medieval feast hall at night, an "
            "immense wooden table running the length of the room set with "
            "iron candelabras and untouched goblets, rows of empty carved "
            "chairs on either side, one chair at the head of the table "
            "still pushed back as if someone just stood, tapestries "
            "depicting old battles hanging on the stone walls, a massive "
            "fireplace roaring at the far end. Painterly, cinematic, "
            "hyper-detailed, visually stunning concept art, vertical "
            "composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with a slow dolly forward down the "
            "length of the table toward the roaring fireplace. The "
            "candle flames flicker and gutter, the fire crackles and "
            "throws shifting light across the tapestries. Epic, majestic "
            "dark fantasy mood, not horror. No people appear, no text."
        ),
    },
    {
        "title": "collapsing tower interior",
        "has_people": False,
        "still_prompt": (
            "The interior of a crumbling stone tower seen from the "
            "ground floor looking straight up through its collapsed roof "
            "to a circle of night sky far above, broken wooden floors of "
            "upper levels jutting out at odd angles, a spiral staircase "
            "crumbling away mid-climb, ivy growing thick up the interior "
            "walls, a shaft of moonlight cutting down through the opening "
            "to illuminate a pile of rubble and a rusted fallen bell. "
            "Painterly, cinematic, hyper-detailed, visually stunning "
            "concept art, vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with a slow upward camera tilt, "
            "starting on the fallen bell and rubble and rising through "
            "the broken floors to the circle of sky above. The shaft of "
            "moonlight shifts slightly, ivy leaves tremble, dust drifts "
            "in the light. Epic, majestic dark fantasy mood, not horror. "
            "No people appear, no text."
        ),
    },
    {
        "title": "the siege line at dawn",
        "has_people": True,
        "still_prompt": (
            "A wide dawn landscape shot: an army encampment of ragged "
            "tents and dying campfires spread across a valley floor, "
            "distant small figures of soldiers moving between the tents, "
            "siege towers and catapults silhouetted against the rising "
            "sun, a besieged castle looming on a hilltop in the distance "
            "with smoke still rising from one damaged wall, mist pooling "
            "in the low ground between camp and castle. Painterly, "
            "cinematic, hyper-detailed, visually stunning concept art, "
            "vertical composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with a slow pull-back, rising and "
            "widening from the campfires to take in the full siege line "
            "and castle. Campfire smoke drifts, mist rolls across the low "
            "ground, distant figures continue their slow movement between "
            "tents. Epic, majestic dark fantasy mood, not horror. No new "
            "people appear, no text."
        ),
    },
    {
        "title": "the drowned library",
        "has_people": False,
        "still_prompt": (
            "A grand stone library half-flooded with still black water, "
            "towering shelves of ruined books rising up out of the "
            "water on either side, a single preserved tome left open on "
            "a floating lectern near the center, shafts of pale light "
            "falling from high arched windows, dust and fine debris "
            "suspended in the still air, a spiral staircase vanishing "
            "into the water at its base. No people. Painterly, cinematic, "
            "hyper-detailed, visually stunning concept art, vertical "
            "composition, no text."
        ),
        "animate_prompt": (
            "Bring this image to life with a slow orbital drift to the "
            "left around the floating lectern, the open tome's pages "
            "stirring faintly as if in a breath of air, dust motes "
            "drifting through the light shafts, the water's surface "
            "rippling very slightly. Epic, majestic dark fantasy mood, "
            "not horror. No people appear, no text."
        ),
    },
]

        ),
    },
