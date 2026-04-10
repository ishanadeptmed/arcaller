# arcaller

Generate reminder audio and optionally trigger a Twilio voicemail-style call that plays the generated recording.

## Setup

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Copy secrets template:
   - Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
3. Fill in your Twilio credentials and config in `.streamlit/secrets.toml`.

## Twilio Secrets

The app reads config from Streamlit secrets first, then environment variables.

Required for voicemail call:
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_FROM_NUMBER`
- `PUBLIC_AUDIO_BASE_URL`

`PUBLIC_AUDIO_BASE_URL` must point to a public URL where the generated wav file can be fetched by Twilio.

## Run

- `streamlit run app.py`

## Notes

- The app generates the audio locally, then Twilio plays it by URL.
- If your audio files are local-only, Twilio cannot access them. Use a public host for the output files.
