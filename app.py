import streamlit as st
from calling import handle_audio_generation

# 1. Page Configuration
st.set_page_config(
    page_title="Nursing Facility Voice Agent", 
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Resident Billing Update Generator")
st.markdown("Enter details below to generate a professional voice reminder using the Kokoro TTS engine.")

# 2. Input Form
with st.form("script_data"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Contacts")
        your_name = st.text_input("Your Name", placeholder="Jane Doe")
        recipient_name = st.text_input("Recipient Name", placeholder="Mr. Smith")
        resident_name = st.text_input("Resident's Name", placeholder="Alice Smith")
    
    with col2:
        st.subheader("Facility & Callback")
        facility_name = st.text_input("Facility Name", placeholder="Birch at Sutherland")
        callback_number = st.text_input("Callback Phone", placeholder="555-0123")

    submit = st.form_submit_button("Generate Professional Audio")

# 3. Logic Execution
if submit:
    # Validation: Ensure no fields are empty
    if not all([your_name, recipient_name, resident_name, facility_name, callback_number]):
        st.warning("⚠️ Please fill in all fields to generate the complete script.")
    else:
        # This calls the function in calling.py which handles the 
        # dictionary creation and the call to templates/converter.py
        handle_audio_generation(
            recipient=recipient_name,
            sender=your_name,
            facility=facility_name,
            resident=resident_name,
            phone=callback_number
        )

# 4. Footer/Instructions for Azure
st.divider()
st.caption("Deployment Note: Ensure 'templates/converter.py' and 'calling.py' are in the root directory.")