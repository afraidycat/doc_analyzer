# Document Analysis Tool

A tool that analyzes documents using AI to provide structured summaries, key topics, risks, and recommended actions.

## Features

- PDF document analysis
- Structured output with summaries, key topics, risks, and actions
- Quality evaluation with automatic retry on subpar results
- Simple web interface using Gradio

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   MODEL_NAME=gpt-4  # or your preferred model
   ```

## Usage

Run the application:
```bash
python -m single_doc_analyze.main
```

Then open your browser to the URL shown in the terminal (typically http://localhost:7860).

## Project Structure

- `main.py`: Entry point and Gradio interface
- `services/`: Core analysis and evaluation services
- `models/`: Pydantic models for data validation
- `utils/`: Utility functions
- `prompts/`: Prompt templates
- `config.py`: Configuration settings

## Error Handling

The application includes comprehensive error handling for:
- PDF processing errors
- API communication issues
- JSON parsing errors
- Invalid responses

All errors are logged and presented to the user in a friendly format. 