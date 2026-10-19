# Speak-Right

#### Video Demo: https://youtu.be/vGMBIbbeBd0

#### Description:

Speak-Right is a Python-based English pronunciation practice application developed for CS50's Introduction to Programming with Python.

The application allows users to create accounts, log in, and practice English words across three difficulty levels: Beginner, Intermediate, and Advanced. Users can listen to a reference pronunciation, record themselves, and receive a score based on the acoustic similarity between their recording and the reference audio.

Speak-Right also stores practice history and provides statistics to help users track their progress. Its weak-word feature identifies words with lower average scores, allowing users to focus on areas where they may need additional practice.

## Design and Implementation

I divided the application into separate Python modules to keep its components organised and make the code easier to maintain.

### `project.py`

This is the application's entry point. Its `main()` function initializes the database and displays the registration, login, and exit menu. After a successful login, the user can access the dashboard to practise words, view statistics, review practice history, and identify weak words.

### `auth.py`

This module handles user registration and login. Passwords are hashed before being stored, so the application does not save them as plain text.

### `database.py`

This module manages SQLite database operations. It creates the required tables, manages user records, loads vocabulary, and stores practice attempts.

The database contains information about users, available words, and practice history. The database file is created locally when the application initializes the database.

### `practice.py`

This module manages the pronunciation practice session. Users select a difficulty level, receive a word from the corresponding vocabulary list, and record their pronunciation.

The recording is evaluated, and the resulting score and attempt details are saved to the database.

### `speech.py`

This module handles audio recording, text-to-speech, and speech recognition.

- `speak()` uses `pyttsx3` to read a target word aloud.
- `generate_reference()` generates reference audio for comparison.
- `record_audio()` captures audio through the microphone using `sounddevice`.
- `verify_word()` uses Google's speech recognition service to obtain a transcription of the recording.

I chose `sounddevice` for audio recording rather than `pyaudio` because it suited my development environment and avoided the installation difficulties I got with `pyaudio`.

### `utils.py`

This module contains the audio comparison and supporting utility functions.

The application extracts Mel-Frequency Cepstral Coefficients (MFCCs) from the reference audio and the user's recording using `librosa`. These features represent aspects of the audio's spectral characteristics.

Dynamic Time Warping (DTW) aligns the two sequences and calculates their distance, allowing the comparison to account for differences in speaking speed and duration.

The distance is converted into a score between 0 and 100. A smaller distance produces a higher score.

The application also uses `rapidfuzz` to compare the recognized transcription with the target word.

The scoring logic combines acoustic similarity with transcription verification:

- If speech recognition returns no usable transcription, the attempt receives a score of zero.
- If the recognized word does not match the target, the score is capped at 20.
- If the recognized word matches the target, the acoustic similarity score is used.

These checks help prevent some incorrect-word attempts from receiving high scores solely because their acoustic features happen to be similar.

### `stats.py`

This module displays performance statistics, practice history, and weak words.

Users can review their previous attempts and examine their scores. Words with an average score below 70% are classified as weak words.

## Limitations and Design Decisions

### Acoustic similarity is not the same as pronunciation accuracy

MFCC and DTW provide a computationally practical way to compare audio recordings. However, the resulting score is an estimate of acoustic similarity, not a validated measure of pronunciation quality.

The reference audio is generated using text-to-speech. Differences in voice, pitch, accent, and speaking style can therefore affect the score even when a word is understandable.

For this reason, Speak-Right should be considered a pronunciation practice aid rather than a professional pronunciation assessment system.

### Speech recognition limitations

The speech recognition component provides an additional check on the spoken word. However, speech recognition systems can infer the intended word even when the pronunciation is imperfect.

Recognition can also fail for uncommon or complex words, accents, and recordings with background noise. Consequently, transcription verification cannot guarantee that a word was pronounced correctly.

### Why I chose this approach

A more advanced pronunciation assessment system could use a phoneme-level speech model. However, such a solution would introduce additional model dependencies, computational requirements, and setup complexity.

I chose MFCC and DTW because they provide a lightweight way to compare recordings while allowing the application to run without downloading a large speech model.

## Project Structure

```text
Speak-Right/
├── project.py
├── test_project.py
├── auth.py
├── database.py
├── practice.py
├── speech.py
├── utils.py
├── stats.py
├── requirements.txt
└── words/
    ├── beginner.txt
    ├── intermediate.txt
    └── advanced.txt
```

The `pronunciation.db` database file is generated locally when the application initializes the database.

## Requirements

- Python
- A working microphone
- The packages listed in `requirements.txt`
- An internet connection for Google's speech recognition service

## How to Run

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Start the application:

```bash
python project.py
```

Follow the on-screen prompts to register, log in, and begin practising.

## Running the Tests

Run the test suite with:

```bash
python -m pytest test_project.py -v
```

The tests cover utility functions and selected functions defined in `project.py`.

## Future Improvements

Potential improvements include more reliable pronunciation assessment, phoneme-level feedback, better handling of speech recognition failures, and a larger vocabulary with pronunciation metadata.