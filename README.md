# Niazi Spotify 🚀


# 🎵 AI Song Recognizer

An intelligent song recognition system powered by Google Gemini AI that identifies songs from partial lyrics, broken sentences, or song names.

## Features

- 🎯 Recognizes songs from incomplete information
- 🎬 Provides movie/album details
- 👨‍🎤 Lists artists and composers
- 📝 Displays song descriptions and trivia
- 🌈 Beautiful colored console interface

## Setup

1. Clone the repository
2. Create a virtual environment:

```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
```

3. Install dependencies:

```bash
   pip install -r requirements.txt
```

4. Create `.env` file and add your Google API key:

```
   GOOGLE_API_KEY=your_api_key_here
```

5. Run the application:

```bash
   python app.py
```

## Usage

Simply enter any information about a song:

- Song name
- Partial lyrics
- Broken sentences
- Movie name + song context

The AI will analyze and provide comprehensive song information.

## Technologies

- Python 3.x
- Google Gemini AI API
- python-dotenv
- colorama

## License

MIT License
