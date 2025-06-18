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

4. Set up environment variables:
Create a `.env` file and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

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