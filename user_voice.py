import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.

    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")


# Audio file path where the recorded audio will be saved
audio_file_path = "user_voice_test.mp3"
# Uncomment to record audio
# record_audio(file_path=audio_file_path)

# Setup the Speech to Text (STT) model for transcription  
from groq import Groq

# Ensure your API key is set in your environment variables
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
stt_model = "whisper-large-v3-turbo"


def transcribe(stt_model, audio_filepath):
    """
    Transcribes the given audio file using the specified STT model.

    Args:
    stt_model (str): The speech-to-text model to use.
    audio_filepath (str): Path to the audio file to transcribe.

    Returns:
    str: The transcribed text from the audio.
    """
    client = Groq(api_key=GROQ_API_KEY)
    
    try:
        # Open the audio file in binary mode
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        
        # Return the transcription text
        return transcription.text
    
    except Exception as e:
        logging.error(f"An error occurred during transcription: {e}")
        return None


# Example of calling the transcribe function after recording the audio
# transcription = transcribe(stt_model, audio_filepath=audio_file_path)
# if transcription:
#     logging.info(f"Transcription: {transcription}")
