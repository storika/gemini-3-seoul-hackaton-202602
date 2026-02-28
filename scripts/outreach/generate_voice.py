"""
Generate personalized voice MP3s from scripts using ElevenLabs TTS.
Voice: Lily, Model: eleven_turbo_v2_5
Input: output/scripts/{handle}.txt
Output: output/voice/{handle}.mp3
"""

import os
import pathlib
from elevenlabs import ElevenLabs

from creators import all_creators

SCRIPTS_DIR = pathlib.Path(__file__).parent / "output" / "scripts"
OUTPUT_DIR = pathlib.Path(__file__).parent / "output" / "voice"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Also copy to root for Twilio serving
ROOT_DIR = pathlib.Path(__file__).parent

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

# Lily voice ID (ElevenLabs pre-made)
LILY_VOICE_ID = "pFZP5JQG7iQjIQuC4Bku"
MODEL_ID = "eleven_turbo_v2_5"


def generate_voice(script_text: str, output_path: pathlib.Path) -> pathlib.Path:
    """Generate MP3 from script text using ElevenLabs."""
    audio = client.text_to_speech.convert(
        voice_id=LILY_VOICE_ID,
        text=script_text,
        model_id=MODEL_ID,
        output_format="mp3_44100_128",
    )

    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return output_path


# Map handle to root MP3 filename (matching existing convention)
HANDLE_TO_FILENAME = {
    "jungha.0": "call_hayoung.mp3",
    "jayeonkim_": "call_jayeon.mp3",
    "hwajung95": "call_hwajung.mp3",
    "bling_cuh__": "call_blingchu.mp3",
}


def main():
    print("Generating personalized voice audio...\n")
    for creator in all_creators():
        script_path = SCRIPTS_DIR / f"{creator.handle}.txt"
        if not script_path.exists():
            print(f"  @{creator.handle} — SKIP (no script found, run generate_scripts.py first)")
            continue

        script_text = script_path.read_text(encoding="utf-8")
        print(f"  @{creator.handle} ({creator.name_kr})...", end=" ", flush=True)

        # Generate to output/voice/
        voice_path = OUTPUT_DIR / f"{creator.handle}.mp3"
        generate_voice(script_text, voice_path)

        # Also copy to root dir for Twilio serving
        root_filename = HANDLE_TO_FILENAME.get(creator.handle)
        if root_filename:
            root_path = ROOT_DIR / root_filename
            root_path.write_bytes(voice_path.read_bytes())
            print(f"✓ ({voice_path.stat().st_size // 1024}KB → also saved as {root_filename})")
        else:
            print(f"✓ ({voice_path.stat().st_size // 1024}KB)")

    print(f"\nDone! Voice files saved to {OUTPUT_DIR}/ and root dir")


if __name__ == "__main__":
    main()
