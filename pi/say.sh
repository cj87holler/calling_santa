#!/bin/sh
# Santa voice test: ask OpenAI text-to-speech for one Santa line and play it
# through the Pi's headphone jack. Usage: sh say.sh [voice]   (default: ash)
# Needs OPENAI_API_KEY in the environment. Never prints the key.

VOICE="${1:-ash}"

if [ -z "$OPENAI_API_KEY" ]; then
  echo "No key loaded. Run the 'read -s' key step first."
  exit 1
fi

python3 - "$VOICE" > body.json <<'PY'
import json, sys
print(json.dumps({
    "model": "gpt-4o-mini-tts",
    "voice": sys.argv[1],
    "response_format": "wav",
    "input": "Ho ho ho, Merry Christmas! This is Santa Claus, calling all the "
             "way from the North Pole. Now tell me, have you been good this year?",
    "instructions": "You are a warm, jolly, grandfatherly Santa Claus. Speak "
                    "slowly with a deep, cozy voice and a hearty chuckle.",
}))
PY

echo "Asking OpenAI for Santa's voice ($VOICE)..."
curl -s https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @body.json -o santa.wav

SIZE=$(wc -c < santa.wav)
if [ "$SIZE" -lt 10000 ]; then
  echo "That didn't come back as audio. OpenAI said:"
  cat santa.wav
  echo
  exit 1
fi

echo "Got $SIZE bytes of audio. Playing into the handset..."
aplay -q -D plughw:Headphones santa.wav
