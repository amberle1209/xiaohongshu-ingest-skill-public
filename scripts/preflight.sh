#!/usr/bin/env bash
set -u

strict=false
requirements=()

while (($#)); do
  case "$1" in
    --strict)
      strict=true
      ;;
    --require)
      shift
      if (($# == 0)); then
        printf '%s\n' 'error: --require needs a capability name' >&2
        exit 2
      fi
      requirements+=("$1")
      ;;
    --help|-h)
      printf '%s\n' 'Usage: preflight.sh [--strict] [--require capability]...'
      printf '%s\n' 'Capabilities: curl, rg, yt-dlp, ffmpeg, lark-cli, faster-whisper'
      exit 0
      ;;
    *)
      printf 'error: unknown argument: %s\n' "$1" >&2
      exit 2
      ;;
  esac
  shift
done

missing_required=0

check_command() {
  local name="$1"
  if command -v "$name" >/dev/null 2>&1; then
    printf 'available: %s (%s)\n' "$name" "$(command -v "$name")"
  else
    printf 'missing: %s\n' "$name"
  fi
}

is_available() {
  case "$1" in
    faster-whisper)
      command -v "$python_bin" >/dev/null 2>&1 && "$python_bin" -c 'import faster_whisper' >/dev/null 2>&1
      ;;
    *) command -v "$1" >/dev/null 2>&1 ;;
  esac
}

printf '%s\n' 'Content ingest capability preflight'
check_command curl
check_command rg
check_command yt-dlp
check_command ffmpeg
check_command lark-cli

python_bin="${WHISPER_PYTHON:-python3}"
if command -v "$python_bin" >/dev/null 2>&1; then
  if "$python_bin" -c 'import faster_whisper' >/dev/null 2>&1; then
    printf 'available: faster_whisper (%s)\n' "$python_bin"
  else
    printf 'missing: faster_whisper (%s)\n' "$python_bin"
  fi
else
  printf 'missing: Python interpreter (%s)\n' "$python_bin"
fi

if "$strict"; then
  requirements+=(curl rg)
fi

for capability in "${requirements[@]}"; do
  if is_available "$capability"; then
    printf 'required capability available: %s\n' "$capability"
  else
    printf 'required capability missing: %s\n' "$capability" >&2
    missing_required=1
  fi
done

printf '%s\n' 'Review config.example.yaml and keep real configuration outside the repository.'
exit "$missing_required"
