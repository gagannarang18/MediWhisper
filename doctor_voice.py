import os
import subprocess
import platform
from gtts import gTTS
import pygame
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

# Function to play the audio
def play_audio(output_filepath):
    """
    Plays the generated audio file based on the operating system.
    Uses pygame for MP3 files.
    """
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            pygame.mixer.init()
            pygame.mixer.music.load(output_filepath)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():  # Wait until the sound finishes
                pygame.time.Clock().tick(10)
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# Function to convert MP3 to WAV (if needed)
def convert_mp3_to_wav(mp3_filepath, wav_filepath):
    """
    Convert MP3 file to WAV file.
    """
    audio = AudioSegment.from_mp3(mp3_filepath)
    audio.export(wav_filepath, format="wav")

# Function for gTTS text-to-speech
def text_to_speech_gtts(input_text, output_filepath):
    """
    Convert text to speech using gTTS and save the output as an MP3 file.
    """
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)
    
    # Play the generated audio
    play_audio(output_filepath)

# Function for ElevenLabs text-to-speech
def text_to_speech_elevenlabs(input_text, output_filepath):
    """
    Convert text to speech using ElevenLabs API and save the output as an MP3 file.
    """
    ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    
    # The generate function returns a response object, which we can read as binary
    audio_generator = client.generate(
        text=input_text,
        voice="Charlie",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    
    # Write the binary audio data to the output file
    with open(output_filepath, 'wb') as f:
        # Iterate through the generator and write the bytes to the file
        for chunk in audio_generator:
            f.write(chunk)
    
    # Play the generated audio
    play_audio(output_filepath)

# Sample input text
# input_text = "Hello how are you doing Mr. Gagan?"

# # Example usage: gTTS Text to Speech
# text_to_speech_gtts(input_text, output_filepath="gtts_testing.mp3")

# # Example usage: ElevenLabs Text to Speech
# text_to_speech_elevenlabs(input_text, output_filepath="elevenlabs_testing.mp3")
