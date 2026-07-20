# Transcription fidelity

## Preserve evidence first

Save the timestamped ASR output without editing it. When producing a corrected reading, keep the original line and add a separate annotation.

```markdown
[12.0s-16.4s] <original ASR text>
Correction: <candidate technical term> — confidence: high | medium | low
Evidence: <caption keyword, visible slide, or repeated contextual cue>
```

## Language selection

Start with automatic language detection. A Chinese title or caption does not reliably identify the spoken language, especially for technical tutorials. Use a forced-language retry only when a short sample, the detected language, or systematic garbling provides evidence.

## Technical terms

Mixed Chinese-English speech can corrupt product names, acronyms, and framework names while preserving timestamp coverage. Do not use duration alone as a fidelity check.

Use the following confidence standard:

- **high** — a visible slide, source caption, or repeated unambiguous contextual evidence supports the correction;
- **medium** — context strongly supports one interpretation, but no direct source confirms it;
- **low** — ambiguous; preserve the ASR text and state the uncertainty.

Do not use another video, a similar post, or general topic knowledge as proof of a correction for the current source.

## Long recordings

For presentations with dense slides, inspect selected source-resolution frames only when visual claims materially affect the answer. Record frame timestamps and keep visual findings separate from speech transcription.

If the ASR process crashes or returns implausibly short output, keep the failure evidence, retry at most once in a clean run directory, then return a partial result if it still fails.
