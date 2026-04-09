import streamlit as st
import os
# Import the engine from your third file
from templates.converter import generate_audio

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