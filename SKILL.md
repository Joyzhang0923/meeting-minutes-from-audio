---
name: meeting-minutes-from-audio
description: Convert meeting audio or video recordings into accurate Chinese transcripts and high-quality structured meeting minutes. Use when the user provides or references meeting recordings (.mp3, .m4a, .wav, .aac, .flac, .mp4, .mov), asks for speech-to-text, transcription, meeting notes, meeting minutes, action items, decisions, summaries, or wants a workflow that turns spoken meetings into polished minutes.
---

# Meeting Minutes From Audio

## Goal

Turn a meeting recording into a trustworthy transcript and a polished meeting minutes document. Preserve decisions, action items, owners, dates, risks, unresolved questions, and important original wording. Do not invent information that is not supported by the transcript.

## Workflow

1. **Collect inputs**
   - Locate the audio/video file path or attached file.
   - Ask only for missing essentials: meeting topic, expected attendees, target style, or whether to include a full transcript.
   - If the user gives no style, use a concise business Chinese style.

2. **Transcribe**
   - Prefer existing transcript text if the user provides it.
   - Otherwise run `scripts/transcribe_audio.py`:

     ```bash
     python3 scripts/transcribe_audio.py /path/to/meeting.m4a --language zh --output transcript.md
     ```

   - If the script cannot transcribe because no backend is configured, explain the missing dependency and continue only if another transcription tool is available.
   - Keep a clean transcript with timestamps when available. Mark unclear audio as `[听不清]` or `[疑似: ...]`; never silently guess.

3. **Normalize the transcript**
   - Remove filler words only when they do not affect meaning.
   - Keep technical terms, numbers, names, deadlines, and commitments exact.
   - Merge repeated false starts, but preserve meaningful disagreement or uncertainty.
   - Speaker labels are useful, but only assign names when there is evidence. Otherwise use `发言人A/B/C`.

4. **Produce the minutes**
   - Follow `references/minutes-template.md` for the default structure.
   - Reorganize by agenda/topic instead of copying chronological chatter.
   - Separate facts, decisions, action items, open questions, and risks.
   - Include short original quotes only for decisions, commitments, objections, or nuanced wording.

5. **Quality check**
   - Apply `references/quality-checklist.md` before finalizing.
   - Every action item must have an owner or be marked `待确认`.
   - Every date, number, budget, KPI, or external commitment must match the transcript.
   - If the audio quality limits confidence, add a brief `转写说明`.

## Output Defaults

Return one Markdown document unless the user asks for another format:

- `会议纪要`: polished, structured minutes.
- `待办事项`: table with task, owner, deadline, status/notes.
- `待确认问题`: ambiguities, missing owners, unclear dates, or low-confidence transcript sections.
- `关键原话`: only the most decision-relevant quotes.

For long meetings, first provide the minutes and action table, then offer to include the full transcript if needed.

## Style Guidance

- Use clear Chinese headings and short paragraphs.
- Write for a busy manager who did not attend the meeting.
- Prefer precise verbs: `确认`, `决定`, `要求`, `暂缓`, `需补充`, `存在风险`.
- Avoid generic summaries such as `大家进行了讨论`; state what was discussed and what changed.
- Do not fabricate attendees, agenda, conclusions, or owners.
