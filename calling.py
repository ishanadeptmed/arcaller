import streamlit as st
import os
from urllib.parse import quote
from typing import Optional
# Import the engine from your third file
from templates.converter import generate_audio
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from config import get_setting

def handle_audio_generation(recipient, sender, facility, resident, phone):
    """
    This function bridges the UI (app.py) and the Engine (converter.py).
    It packages the data and handles the file display.
    """
    
    # 1. Package the data into the format converter.py expects
    user_data = {
        "recipient_name": recipient,
        "your_name": sender,
        "facility_name": facility,
        "resident_name": resident,
        "phone_number": phone
    }

    # 2. Define where the file should be saved temporarily
    # Using a relative path works best for containerized environments
    output_filename = f"reminder_{resident.replace(' ', '_')}.wav"
    generated_file_path = os.path.join(os.getcwd(), output_filename)

    try:
        # 3. Trigger the Kokoro engine in converter.py
        with st.spinner("Generating professional voice update..."):
            path = generate_audio(user_data, output_path=generated_file_path)
        
        # 4. Success feedback and Audio Player
        if os.path.exists(path):
            st.success("✅ Audio generated successfully!")
            with open(path, 'rb') as f:
                audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/wav")
            
            # Add a download button for the user
            st.download_button(
                label="Download Audio File",
                data=audio_bytes,
                file_name=output_filename,
                mime="audio/wav"
            )
            return path
    except Exception as e:
        st.error(f"An error occurred during generation: {e}")
        return None


def _build_public_audio_url(local_path: str) -> Optional[str]:
    """
    Convert a local audio path into a publicly reachable URL that Twilio can play.
    """
    base_url = get_setting("PUBLIC_AUDIO_BASE_URL")
    if not base_url:
        return None

    filename = os.path.basename(local_path)
    return f"{base_url.rstrip('/')}/{quote(filename)}"


def send_voicemail_drop(local_audio_path: str, recipient_phone: str) -> Optional[str]:
    """
    Trigger a Twilio outbound call and play the generated audio.
    This is intended for voicemail delivery workflows.
    """
    account_sid = get_setting("TWILIO_ACCOUNT_SID")
    auth_token = get_setting("TWILIO_AUTH_TOKEN")
    from_number = get_setting("TWILIO_FROM_NUMBER")

    if not account_sid or not auth_token or not from_number:
        st.error(
            "Twilio config is missing. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, "
            "and TWILIO_FROM_NUMBER in secrets."
        )
        return None

    audio_url = _build_public_audio_url(local_audio_path)
    if not audio_url:
        st.error(
            "PUBLIC_AUDIO_BASE_URL is missing in secrets. "
            "Twilio must access your audio over a public URL."
        )
        return None

    twiml = f"""
    <Response>
        <Play>{audio_url}</Play>
    </Response>
    """.strip()

    try:
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            to=recipient_phone,
            from_=from_number,
            twiml=twiml,
            machine_detection="DetectMessageEnd",
            timeout=30,
        )
        return call.sid
    except TwilioRestException as exc:
        st.error(f"Twilio call failed: {exc.msg}")
        return None