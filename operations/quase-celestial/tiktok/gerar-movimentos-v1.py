from pathlib import Path

from tools.video.seedance_video import SeedanceVideo


ROOT = Path(__file__).resolve().parent

JOBS = [
    (
        "001-nao-estou-atrasada",
        "Keep the reference composition and the same clearly young adult woman from behind. A gentle breeze moves her hair and dark jacket; distant city lights softly pulse; a few lavender particles drift upward; very slow cinematic push-in. She remains facing the horizon. No face reveal, no new people, no text, no camera shake, no sudden action, no audio.",
    ),
    (
        "002-deixar-o-dia-ir",
        "Keep the reference composition and the same clearly young adult woman at the window. The sheer curtain gently breathes in a night breeze; moonlight trembles softly on the water; violet dust motes float through the room; tiny lamp flame flicker. The woman remains still and her face stays hidden. No new people, no text, no camera shake, no sudden action, no audio.",
    ),
    (
        "003-eu-me-permito-querer-mais",
        "Keep the reference composition and the same clearly young adult woman walking into the flower field. Wildflowers sway gently; warm apricot light inside the doorway flickers softly; a few stars and light particles drift in the blue-violet sky; her hair moves very slightly; slow forward cinematic motion. Her face remains hidden. No new people, no text, no camera shake, no sudden action, no audio.",
    ),
]

tool = SeedanceVideo()
for episode_id, prompt in JOBS:
    episode_dir = ROOT / episode_id
    output_path = episode_dir / "movimento-cenario-v1-seedance-5s.mp4"
    if output_path.exists():
        print({"episode": episode_id, "status": "already_generated"}, flush=True)
        continue

    result = tool.execute(
        {
            "prompt": prompt,
            "operation": "image_to_video",
            "model_variant": "standard",
            "duration": "5",
            "aspect_ratio": "9:16",
            "resolution": "720p",
            "generate_audio": False,
            "image_path": str(episode_dir / "arte-master-v1.png"),
            "output_path": str(output_path),
            "seed": 170324,
        }
    )
    print(
        {
            "episode": episode_id,
            "success": result.success,
            "cost_usd": result.cost_usd,
            "output": str(output_path),
            "error": result.error,
        },
        flush=True,
    )
    if not result.success:
        raise RuntimeError(result.error or "Seedance generation failed")
