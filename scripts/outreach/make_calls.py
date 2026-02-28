"""
Make Twilio calls with personalized audio via localtunnel.
Serves the root MP3 files (call_hayoung.mp3 etc.) through localtunnel on port 8889.

Prerequisites:
- localtunnel running: lt --port 8889
- HTTP server: python3 -m http.server 8889 (from hackathon-voice-demo dir)
- Personalized MP3s generated (run generate_voice.py first)
"""

import os
import sys
import json
import subprocess
import time
from twilio.rest import Client

from creators import all_creators

TWILIO_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_FROM = "+14069646762"

client = Client(TWILIO_SID, TWILIO_TOKEN)

# Map creator handle → MP3 filename served by localtunnel
HANDLE_TO_FILE = {
    "jungha.0": "call_hayoung.mp3",
    "jayeonkim_": "call_jayeon.mp3",
    "hwajung95": "call_hwajung.mp3",
    "bling_cuh__": "call_blingchu.mp3",
}

# Demo phone numbers (team members standing in for creators)
DEMO_PHONES = {
    "jungha.0": "",    # Fill with team phone for demo
    "jayeonkim_": "",
    "hwajung95": "",
    "bling_cuh__": "",
}


def get_tunnel_url() -> str:
    """Get the active localtunnel URL. Falls back to prompt."""
    # Try to detect from running lt process
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:8889/call_hayoung.mp3", "--head"],
            capture_output=True, timeout=5,
        )
        if result.returncode == 0:
            print("  Local server confirmed running on port 8889")
    except Exception:
        pass

    url = os.environ.get("TUNNEL_URL", "")
    if not url:
        url = input("Enter localtunnel URL (e.g. https://xxx.loca.lt): ").strip()
    return url.rstrip("/")


def make_call(to_number: str, audio_url: str, creator_name: str) -> str | None:
    """Place a Twilio call that plays the personalized audio."""
    twiml = f"""<Response>
    <Play>{audio_url}</Play>
    <Pause length="2"/>
    <Say language="ko-KR">감사합니다. 좋은 하루 되세요.</Say>
</Response>"""

    try:
        call = client.calls.create(
            to=to_number,
            from_=TWILIO_FROM,
            twiml=twiml,
        )
        return call.sid
    except Exception as e:
        print(f"  ERROR calling {creator_name}: {e}")
        return None


def main():
    print("=== Personalized Voice Outreach ===\n")

    # Check for phone numbers
    if not any(DEMO_PHONES.values()):
        print("No phone numbers configured. Options:")
        print("  1. Edit DEMO_PHONES in make_calls.py")
        print("  2. Pass numbers as args: python make_calls.py +1234567890 +0987654321 ...")
        print("  3. Run in demo mode (just verify audio URLs)\n")

        if len(sys.argv) > 1:
            phones = sys.argv[1:]
            handles = list(HANDLE_TO_FILE.keys())
            for i, phone in enumerate(phones):
                if i < len(handles):
                    DEMO_PHONES[handles[i]] = phone

    tunnel_url = get_tunnel_url()
    print(f"\nTunnel URL: {tunnel_url}\n")

    results = []
    for creator in all_creators():
        handle = creator.handle
        mp3_file = HANDLE_TO_FILE.get(handle)
        if not mp3_file:
            continue

        audio_url = f"{tunnel_url}/{mp3_file}"
        phone = DEMO_PHONES.get(handle, "")

        print(f"@{handle} ({creator.name_kr}):")
        print(f"  Audio: {audio_url}")

        if phone:
            print(f"  Calling: {phone}...", end=" ", flush=True)
            sid = make_call(phone, audio_url, creator.name_kr)
            if sid:
                print(f"✓ (SID: {sid})")
                results.append({"handle": handle, "phone": phone, "sid": sid, "status": "initiated"})
            else:
                results.append({"handle": handle, "phone": phone, "sid": None, "status": "failed"})
        else:
            print("  No phone number — skipping call (audio URL verified)")
            results.append({"handle": handle, "phone": None, "sid": None, "status": "no_phone"})
        print()

    # Summary
    print("=== Call Summary ===")
    for r in results:
        status = "📞 Called" if r["status"] == "initiated" else "⏭ Skipped"
        print(f"  {status} @{r['handle']}")

    return results


if __name__ == "__main__":
    main()
