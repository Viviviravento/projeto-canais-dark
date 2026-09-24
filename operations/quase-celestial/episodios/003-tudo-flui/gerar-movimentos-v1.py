from pathlib import Path

from tools.video.seedance_video import SeedanceVideo


EPISODE = Path(__file__).resolve().parent

JOBS = [
    (
        "arte-master-v1-manha-verde.png",
        "movimento-cena-v1-manha-verde-seedance-5s.mp4",
        "Keep the exact reference composition and the same clearly adult woman with short curly dark hair, sitting in the sunlit meadow and reading. A warm summer breeze visibly sways the flowering branch in the near upper-left foreground and the tall grass in the foreground; a few tiny wildflower petals drift sideways. Her shirt and hair move naturally only a little. Slow, smooth cinematic lateral camera drift through the grass with a soft push-in. The woman remains quiet and no face is revealed. Peaceful but clearly alive, not a static photograph. No new people, no text, no logo, no camera shake, no sudden motion, no audio.",
    ),
    (
        "arte-master-v2-litoral-turquesa.png",
        "movimento-cena-v2-litoral-turquesa-seedance-5s.mp4",
        "Keep the exact reference composition and the same clearly adult woman in a coral shirt seated on the coastal rock looking at the ocean. A more noticeable but calm sea breeze sways the tall foreground grass and the leafy branch close to the top-right lens; small waves visibly roll and dissolve on the rocks. Loose hair strands and her shirt move naturally a little. Slow smooth cinematic drift toward the turquoise water, no face reveal. Peaceful, poetic, and clearly animated, never frantic. No new people, no text, no logo, no camera shake, no sudden action, no audio.",
    ),
]

tool = SeedanceVideo()
for image_name, output_name, prompt in JOBS:
    output_path = EPISODE / "arte" / output_name
    if output_path.exists():
        print({"output": str(output_path), "status": "already_generated"}, flush=True)
        continue
    result = tool.execute(
        {
            "prompt": prompt,
            "operation": "image_to_video",
            "model_variant": "standard",
            "duration": "5",
            "aspect_ratio": "16:9",
            "resolution": "720p",
            "generate_audio": False,
            "image_path": str(EPISODE / "arte" / image_name),
            "output_path": str(output_path),
            "seed": 170324,
        }
    )
    print({"output": str(output_path), "success": result.success, "cost_usd": result.cost_usd, "error": result.error}, flush=True)
    if not result.success:
        raise RuntimeError(result.error or "Seedance generation failed")
