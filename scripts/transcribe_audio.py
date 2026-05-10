#!/usr/bin/env python3
"""Transcribe meeting audio with an available backend.

Backends:
- openai: requires OPENAI_API_KEY and the openai Python package.
- whisper-cli: requires the local `whisper` command.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def transcribe_openai(audio_path: Path, language: str | None, model: str) -> str:
    try:
        from openai import OpenAI
    except Exception as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("openai Python package is not installed") from exc

    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set")

    client = OpenAI()
    with audio_path.open("rb") as audio_file:
        kwargs = {
            "model": model,
            "file": audio_file,
            "response_format": "text",
        }
        if language:
            kwargs["language"] = language
        result = client.audio.transcriptions.create(**kwargs)
    return str(result).strip()


def transcribe_whisper_cli(audio_path: Path, language: str | None) -> str:
    whisper = shutil.which("whisper")
    if not whisper:
        raise RuntimeError("whisper CLI is not installed")

    with tempfile.TemporaryDirectory() as tmp:
        cmd = [
            whisper,
            str(audio_path),
            "--task",
            "transcribe",
            "--output_format",
            "txt",
            "--output_dir",
            tmp,
        ]
        if language:
            cmd.extend(["--language", language])
        subprocess.run(cmd, check=True)
        txt_files = sorted(Path(tmp).glob("*.txt"))
        if not txt_files:
            raise RuntimeError("whisper CLI completed but produced no .txt file")
        return txt_files[0].read_text(encoding="utf-8").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcribe meeting audio.")
    parser.add_argument("audio", type=Path, help="Path to audio/video file")
    parser.add_argument("--output", type=Path, default=Path("transcript.md"))
    parser.add_argument("--language", default="zh", help="ISO language hint, e.g. zh or en")
    parser.add_argument("--backend", choices=["auto", "openai", "whisper-cli"], default="auto")
    parser.add_argument("--model", default="whisper-1", help="OpenAI transcription model")
    args = parser.parse_args()

    audio_path = args.audio.expanduser().resolve()
    if not audio_path.exists():
        print(f"Audio file not found: {audio_path}", file=sys.stderr)
        return 2

    errors: list[str] = []
    backends = [args.backend] if args.backend != "auto" else ["openai", "whisper-cli"]

    transcript = None
    for backend in backends:
        try:
            if backend == "openai":
                transcript = transcribe_openai(audio_path, args.language, args.model)
            elif backend == "whisper-cli":
                transcript = transcribe_whisper_cli(audio_path, args.language)
            break
        except Exception as exc:
            errors.append(f"{backend}: {exc}")

    if transcript is None:
        print("No transcription backend succeeded.", file=sys.stderr)
        print(json.dumps(errors, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(transcript + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
