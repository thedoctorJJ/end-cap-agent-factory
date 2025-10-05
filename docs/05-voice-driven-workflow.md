# Voice-Driven Workflow Design

## Overview
Enables PRD submission via voice or text, converted into structured JSON and sent to Devin AI for agent creation.

## Workflow Stages
| Stage | Description |
|-------|-------------|
| Voice Capture | User speaks into microphone or uploads audio |
| Speech-to-Text | Whisper converts audio → text |
| GPT-5 Refinement | Converts transcript → structured PRD |
| PRD Storage | Supabase stores PRD and triggers MCP service |
| Agent Orchestration | Devin AI reads PRD and creates agents |
| Feedback | Optional TTS reads confirmation/status back to user |

## Data Flow
```
[User Voice Input] --> Whisper
↓
[Raw Text] --> GPT-5
↓
[Structured PRD JSON] --> Supabase
↓
[Trigger MCP Service] --> New GitHub Repo
↓
[Devin AI] --> Agents & Orchestration
↓
[FastAPI Backend] --> Next.js Dashboard
```

## Principles
- PRD data handled via APIs, not raw voice
- End-to-end automation with real-time feedback
- Modular and repeatable
