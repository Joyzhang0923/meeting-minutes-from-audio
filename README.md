# Meeting Minutes From Audio

An OpenClaw/Codex skill for turning meeting audio or video recordings into accurate transcripts and structured Chinese meeting minutes.

## What It Does

This skill helps an agent:

- Transcribe meeting recordings from audio or video files
- Clean and normalize the transcript without changing meaning
- Extract decisions, action items, owners, deadlines, risks, and open questions
- Produce polished Chinese meeting minutes in Markdown
- Preserve important original quotes when they affect decisions or commitments

## Repository Structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── minutes-template.md
│   └── quality-checklist.md
└── scripts/
    └── transcribe_audio.py
```

## Installation

Clone or copy this repository into your OpenClaw/Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/Joyzhang0923/meeting-minutes-from-audio.git ~/.codex/skills/meeting-minutes-from-audio
```

After installation, invoke it with:

```text
Use $meeting-minutes-from-audio to transcribe this meeting audio and produce structured meeting minutes.
```

## Transcription Backends

The bundled script supports two transcription backends:

1. OpenAI audio transcription API
2. Local `whisper` command line tool

### OpenAI Backend

Install the OpenAI Python package and set your API key:

```bash
pip install openai
export OPENAI_API_KEY="your_api_key"
```

Then run:

```bash
python3 scripts/transcribe_audio.py /path/to/meeting.m4a --language zh --output transcript.md
```

### Local Whisper Backend

If you have the `whisper` CLI installed, the script can use it automatically:

```bash
python3 scripts/transcribe_audio.py /path/to/meeting.m4a --backend whisper-cli --language zh --output transcript.md
```

## Supported Inputs

Typical supported formats include:

- `.mp3`
- `.m4a`
- `.wav`
- `.aac`
- `.flac`
- `.mp4`
- `.mov`

Actual format support depends on the transcription backend available in your environment.

## Default Output

The skill produces a Markdown meeting minutes document with:

- Meeting information
- Executive summary
- Key discussion topics
- Confirmed decisions
- Action items
- Risks and open questions
- Important original quotes
- Transcription notes

## Usage Example

```text
Use $meeting-minutes-from-audio with ./recordings/product-sync.m4a.
Please output a concise Chinese meeting summary with action items and owners.
```

## Notes

- The skill should not invent attendees, conclusions, deadlines, or owners.
- Unclear audio should be marked as `[听不清]` or `[疑似: ...]`.
- Action items without clear owners or deadlines should be marked `待确认`.
- Long meetings should prioritize the structured minutes first, then provide the full transcript only when requested.
