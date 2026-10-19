import speech_recognition as sr
import pyttsx3
import sounddevice as sd
from scipy.io.wavfile import write as write_wav

SAMPLE_RATE = 16000


def speak(text):
    """
    Speaks the given text aloud using text-to-speech.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def record_audio(filepath, duration=3):
    """
    Records audio from the microphone for a fixed duration and saves it as a wav file.
    """
    print("\nSpeak now...\n")

    recording = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )
    sd.wait()
    write_wav(filepath, SAMPLE_RATE, recording)
    return True


def generate_reference(word, filepath):
    """
    Generates a spoken reference pronunciation of a word and saves it as a wav file.
    """
    engine = pyttsx3.init()
    engine.save_to_file(word, filepath)
    engine.runAndWait()
    engine.stop()


def verify_word(filepath):
    """
    Transcribes a recorded WAV file using Google Speech Recognition.
    """
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(filepath) as source:
            audio = recognizer.record(source)

        result = recognizer.recognize_google(
            audio,
            language="en-US",
            show_all=True
        )

        if not result or "alternative" not in result:
            print("Google returned no recognition results.")
            return None

        alternatives = result["alternative"]
        print("Google recognition results:", alternatives)

        return alternatives[0].get("transcript")

    except sr.UnknownValueError:
        print("Google received the audio but couldn't recognise the speech.")
        return None

    except sr.RequestError as error:
        print(f"Google Speech Recognition request failed: {error}")
        return None

    except (OSError, ValueError) as error:
        print(f"Audio file error: {error}")
        return None