# Resume Generator (Python)

Generate professional resumes using the Claude Agent SDK with web search capabilities.

Python port of the [TypeScript resume-generator demo](https://github.com/anthropics/claude-agent-sdk-demos/tree/main/resume-generator).

## Features

- Researches a person using web search (LinkedIn, company pages, news, GitHub)
- Generates a professional 1-page resume as a `.docx` file
- Uses the `docx` npm library (via the agent) for Word document generation

## Prerequisites

- Python 3.10+
- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)
- Node.js (for the `docx` npm library used by the agent)
- `ANTHROPIC_API_KEY` environment variable set

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python resume_generator.py "Person Name"
```

Example:

```bash
python resume_generator.py "Dario Amodei"
```

## How It Works

1. Uses `WebSearch` to research the person's professional background
2. Gathers information about their current role, past experience, education, and skills
3. Generates a JavaScript file that creates the resume using the `docx` library
4. Executes the script to produce a `.docx` file

## Output

The generated resume is saved to `output/resume/dario-amodei.docx`
