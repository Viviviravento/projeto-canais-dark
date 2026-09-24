from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
HELPER_PATH = ROOT / "operations/a-palavra-que-cuida/scripts/build-video-006-shorts.py"
helper_spec = importlib.util.spec_from_file_location("video006_short_builder", HELPER_PATH)
if helper_spec is None or helper_spec.loader is None:
    raise RuntimeError(f"Unable to load helper: {HELPER_PATH}")
helper = importlib.util.module_from_spec(helper_spec)
sys.modules[helper_spec.name] = helper
helper_spec.loader.exec_module(helper)

SOURCE_AUDIO = ROOT / "operations/a-palavra-que-cuida/05_audio/video-007/v1/video-007-narracao-v1-1.07x-master.wav"
ALIGNMENT = ROOT / "operations/a-palavra-que-cuida/05_audio/video-007/v1/master-alignment-1.07x.json"
WORK_ROOT = ROOT / "operations/a-palavra-que-cuida/06_edicao/video-007/shorts"
PROPS_ROOT = WORK_ROOT / "props"
PUBLIC_AUDIO = ROOT / "tools/OpenMontage/remotion-composer/public/video-007-curtos/audio"

helper.SOURCE_AUDIO = SOURCE_AUDIO
helper.ALIGNMENT = ALIGNMENT
helper.PUBLIC_AUDIO = PUBLIC_AUDIO

SegmentSpec = helper.SegmentSpec
VisualSpec = helper.VisualSpec
ScriptureSpec = helper.ScriptureSpec
ShortSpec = helper.ShortSpec


SPECS = (
    ShortSpec(
        short_id="01",
        title="Jesus não despreza a sua fraqueza",
        hook="Jesus não despreza a sua fraqueza",
        segments=(SegmentSpec(
            "Talvez a parte mais acolhedora dessa história seja esta",
            "Mostra o que eu não estou conseguindo enxergar",
        ),),
        visuals=(
            VisualSpec(9.0, "video-007/assets/video-007/images/v02-jesus-no-deserto-v1.png", "20% 50%"),
            VisualSpec(18.0, "video-007/assets/video-007/images/v05-acolhimento-na-sala-v1.png", "40% 50%"),
            VisualSpec(27.0, "video-007/assets/video-007/images/v01-pausa-na-cozinha-com-croche-v1.png", "61% 50%"),
            VisualSpec(36.0, "video-007/assets/video-007/images/v03-pausa-diante-da-pressao-v1.png", "20% 50%"),
            VisualSpec(45.0, "video-007/assets/video-007/images/v04-pausa-no-corredor-v1.png", "22% 50%"),
            VisualSpec(54.0, "video-007/assets/video-007/images/v06-caminho-sem-pressa-v1.png", "50% 50%"),
            VisualSpec(63.0, "video-007/assets/video-007/images/v05-acolhimento-na-sala-v1.png", "40% 50%"),
            VisualSpec(72.0, "video-007/assets/video-007/images/v01-pausa-na-cozinha-com-croche-v1.png", "61% 50%"),
            VisualSpec(999.0, "video-007/assets/video-007/images/v02-jesus-no-deserto-v1.png", "50% 50%"),
        ),
        scriptures=(ScriptureSpec(
            "Porque não temos um sumo sacerdote que não possa compadecer-se",
            "em tudo foi tentado mas sem pecado",
            "Porque não temos um sumo sacerdote que não possa compadecer-se das nossas fraquezas; porém, um que, como nós, em tudo foi tentado, mas sem pecado.",
            "Hebreus 4:15 — ACF",
        ),),
    ),
    ShortSpec(
        short_id="02",
        title="Três perguntas antes de uma escolha urgente",
        hook="Não decida no pior momento do dia",
        segments=(SegmentSpec(
            "Quando você perceber que uma escolha está parecendo urgente demais",
            "está tentando comprar sua paz",
        ),),
        visuals=(
            VisualSpec(9.0, "video-007/assets/video-007/images/v03-pausa-diante-da-pressao-v1.png", "20% 50%"),
            VisualSpec(18.0, "video-007/assets/video-007/images/v04-pausa-no-corredor-v1.png", "22% 50%"),
            VisualSpec(27.0, "video-007/assets/video-007/images/v05-acolhimento-na-sala-v1.png", "40% 50%"),
            VisualSpec(36.0, "video-007/assets/video-007/images/v01-pausa-na-cozinha-com-croche-v1.png", "61% 50%"),
            VisualSpec(45.0, "video-007/assets/video-007/images/v06-caminho-sem-pressa-v1.png", "50% 50%"),
            VisualSpec(54.0, "video-007/assets/video-007/images/v02-jesus-no-deserto-v1.png", "20% 50%"),
            VisualSpec(63.0, "video-007/assets/video-007/images/v04-pausa-no-corredor-v1.png", "22% 50%"),
            VisualSpec(72.0, "video-007/assets/video-007/images/v05-acolhimento-na-sala-v1.png", "40% 50%"),
            VisualSpec(81.0, "video-007/assets/video-007/images/v01-pausa-na-cozinha-com-croche-v1.png", "61% 50%"),
            VisualSpec(999.0, "video-007/assets/video-007/images/v06-caminho-sem-pressa-v1.png", "50% 50%"),
        ),
        scriptures=(),
    ),
)


def main() -> None:
    words = helper.alignment_words()
    PROPS_ROOT.mkdir(parents=True, exist_ok=True)
    PUBLIC_AUDIO.mkdir(parents=True, exist_ok=True)
    outputs: list[dict[str, Any]] = []
    for spec in SPECS:
        selected_segments: list[dict[str, Any]] = []
        for segment in spec.segments:
            start_index, _ = helper.find_phrase(words, segment.start_phrase)
            _, end_index = helper.find_phrase(words, segment.end_phrase)
            selected = words[start_index:end_index + 1]
            selected_segments.append({
                "start": max(0.0, selected[0]["start"] - 0.08),
                "end": selected[-1]["end"] + 0.15,
                "words": selected,
            })
        audio_name = f"video-007-curto-{spec.short_id}-narracao.wav"
        audio_output = PUBLIC_AUDIO / audio_name
        helper.render_audio([(item["start"], item["end"]) for item in selected_segments], audio_output)
        cues: list[dict[str, Any]] = []
        source_windows: list[dict[str, float]] = []
        segment_offsets: list[float] = []
        timeline_offset = 0.0
        for index, segment in enumerate(selected_segments):
            segment_offsets.append(timeline_offset)
            cues.extend(helper.caption_cues(segment["words"], segment["start"], timeline_offset))
            source_windows.append({"start": round(segment["start"], 3), "end": round(segment["end"], 3)})
            timeline_offset += segment["end"] - segment["start"]
            if index < len(selected_segments) - 1:
                timeline_offset += helper.GAP_SECONDS
        spoken_duration = round(timeline_offset, 3)
        if spoken_duration < 60:
            raise ValueError(f"Short {spec.short_id} is only {spoken_duration}s")
        scriptures: list[dict[str, Any]] = []
        for scripture in spec.scriptures:
            start_index, _ = helper.find_phrase(words, scripture.start_phrase)
            _, end_index = helper.find_phrase(words, scripture.end_phrase)
            source_start = words[start_index]["start"]
            source_end = words[end_index]["end"]
            containing_index = next(i for i, segment in enumerate(selected_segments) if segment["start"] <= source_start <= segment["end"])
            segment = selected_segments[containing_index]
            scriptures.append({
                "start": round(segment_offsets[containing_index] + source_start - segment["start"], 3),
                "end": round(segment_offsets[containing_index] + source_end - segment["start"], 3),
                "text": scripture.text,
                "reference": scripture.reference,
            })
        props = {
            "derivativeId": f"video-007-curto-{spec.short_id}",
            "title": spec.title,
            "platform": "universal",
            "audioFile": f"video-007-curtos/audio/{audio_name}",
            "spokenDurationSeconds": spoken_duration,
            "endCardSeconds": 4.0,
            "hook": spec.hook,
            "hookEndSeconds": 4.2,
            "visuals": helper.make_visuals(spec, spoken_duration),
            "cues": cues,
            "scriptures": scriptures,
        }
        props_path = PROPS_ROOT / f"video-007-curto-{spec.short_id}-shorts-e-tiktok.json"
        props_path.write_text(json.dumps(props, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        outputs.append({
            "derivative_id": props["derivativeId"],
            "title": spec.title,
            "source_windows": source_windows,
            "spoken_duration_seconds": spoken_duration,
            "total_duration_seconds": round(spoken_duration + 4.0, 3),
            "audio": str(audio_output.relative_to(ROOT)).replace("\\", "/"),
            "props": str(props_path.relative_to(ROOT)).replace("\\", "/"),
            "platforms": ["youtube_shorts", "tiktok"],
            "paid_api_cost_usd": 0,
        })
    manifest = {
        "schema_version": 1,
        "source_video": "video-007",
        "source_state": "canonical_audio_alignment_and_approved_images_before_long_master_export",
        "rendered_editorial_derivatives": outputs,
        "editorial_derivative_count": 2,
        "physical_mp4_target_count": 2,
        "paid_api_cost_usd": 0,
        "method": "Narração 1.07x aprovada, imagens canônicas e recomposição vertical manual em cover.",
    }
    (WORK_ROOT / "manifest-v1.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
