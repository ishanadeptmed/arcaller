import sys
import os
import soundfile as sf
import numpy as np

# Ensure the local kokoro files are in the path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from kokoro import KPipeline

def generate_audio(data, output_path="/content/output.wav"):
    """
    data: A dictionary containing:
    - 'recipient_name'
    - 'your_name'
    - 'facility_name'
    - 'resident_name'
    - 'phone_number'
    """
    
    # 1. Format the new professional script with dynamic data
    text = (
        f"Hello {data['recipient_name']}, this is {data['your_name']} calling from "
        f"{data['facility_name']} Nursing Facility regarding {data['resident_name']}. "
        f"I’m calling with a quick update regarding the unpaid balance and just need to connect with you briefly. "
        f"Please give me a call back at {data['phone_number']} when you have a moment. "
        f"Again, this is {data['your_name']} from {data['facility_name']}, and my number is {data['phone_number']}. "
        f"Thank you and I look forward to speaking with you."
    )

    # 2. Initialize the Kokoro Pipeline
    pipeline = KPipeline(lang_code='a')

    # 3. Generate generator object
    generator = pipeline(
        text,
        voice='af_heart',  # Your preferred high-quality voice
        speed=1
    )

    full_audio = []

    # 4. Process the stream of audio chunks
    for _, (_, _, audio) in enumerate(generator):
        full_audio.append(audio)

    # 5. Combine chunks into one final clip
    final_audio = np.concatenate(full_audio)

    # 6. Ensure directory exists and write file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, final_audio, 24000)

    return output_path