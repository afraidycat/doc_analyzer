# Multi-Agent Document Analysis System

A system of AI agents that work together to analyze documents and simulate fee structures. The system includes:

## Components

### Document Analysis Agent
- PDF document analysis
- Structured output with summaries, key topics, risks, and actions
- Quality evaluation with automatic retry on subpar results
- Simple web interface using Gradio

### Fee Simulator Agent
- Fee structure analysis and simulation
- Integration with document analysis for comprehensive evaluation

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

### Document Analysis
Run the document analysis interface:
```bash
python -m single_doc_analyze.main
```

### Fee Simulation
Run the fee simulator:
```bash
python -m fee_simulator.main
```

## Project Structure

- `single_doc_analyze/`: Document analysis agent
  - `main.py`: Entry point and Gradio interface
  - `services/`: Core analysis and evaluation services
  - `models/`: Pydantic models for data validation
  - `utils/`: Utility functions
  - `prompts/`: Prompt templates
  - `config.py`: Configuration settings

- `fee_simulator/`: Fee simulation agent
  - `main.py`: Fee simulation interface and logic

## Error Handling

The application includes comprehensive error handling for:
- PDF processing errors
- API communication issues
- JSON parsing errors
- Invalid responses
- Fee calculation errors

All errors are logged and presented to the user in a friendly format.

## Testing

Run the test suite:
```bash
pytest
```

The test suite includes:
- Unit tests for document analysis
- Unit tests for fee simulation
- Integration tests for agent interaction 