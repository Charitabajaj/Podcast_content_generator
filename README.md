# Podcast Content Generator

A modern web application for generating podcast content using Google's Gemini AI. This tool helps podcast creators generate research analysis, interview questions, and episode titles.

## Features

- Content Research & Analysis
  - Current Trends Analysis
  - Competitor Content Analysis
  - Audience Interest Analysis
  - Content Gap Analysis

- Interview Questions Generation
  - Deep Dive Questions
  - Casual Conversation Questions
  - Educational Questions

- Episode Title Generation
  - Multiple title suggestions
  - Different style options

## Tech Stack

- Python
- Flask
- Google Gemini AI
- HTML/CSS
- JavaScript

## Setup

1. Clone the repository:
```bash
git clone https://github.com/Charitabajaj/Podcast_content_generator.git
cd Podcast_content_generator
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Gemini API key:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Open `config.yaml` and replace `YOUR_GEMINI_API_KEY_HERE` with your actual API key

5. Run the application:
```bash
python app.py
```

## Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Choose the type of content you want to generate
3. Fill in the required fields
4. Click generate and wait for the AI to create your content

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 