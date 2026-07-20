# Xiaohongshu extraction

## Video posts

Probe the extractor before downloading. Create the run directory first, validate the public redirect chain, collect metadata, then download media only when transcription or media inspection is required. Set `SOCKET_TIMEOUT`, `TOTAL_TIMEOUT`, `MAX_REDIRECTS`, and `MAX_DOWNLOAD_BYTES` from the active configuration.

```bash
CANONICAL_URL="$(python3 scripts/validate_public_url.py \
  --max-redirects "$MAX_REDIRECTS" "$URL")"
python3 scripts/run_with_timeout.py "$TOTAL_TIMEOUT" -- \
  yt-dlp --dump-single-json --no-playlist \
  --socket-timeout "$SOCKET_TIMEOUT" --retries 1 \
  --max-filesize "$MAX_DOWNLOAD_BYTES" \
  "$CANONICAL_URL" > "$RUN_DIR/meta.json"
python3 scripts/run_with_timeout.py "$TOTAL_TIMEOUT" -- \
  yt-dlp --no-playlist --write-info-json \
  --socket-timeout "$SOCKET_TIMEOUT" --retries 1 --fragment-retries 1 \
  --max-filesize "$MAX_DOWNLOAD_BYTES" \
  --paths "$RUN_DIR" \
  --output '%(id)s.%(ext)s' \
  "$CANONICAL_URL"
```

`validate_public_url.py` connects to a vetted public address for every navigation redirect, but it cannot sandbox every media request made internally by an extractor. Use this recipe only for supported public sources, validate the final metadata URL, and report extractor-level redirect limits that cannot be independently observed. Validate the final media path and duration from the resulting metadata. Do not assume that metadata-only extraction produced an MP4.

Transcribe with automatic language detection first:

```python
from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe(media_path, language=None, beam_size=5)
transcript = [f"[{segment.start:.1f}s-{segment.end:.1f}s] {segment.text}" for segment in segments]
```

Do not set `language="zh"` merely because a title or description is Chinese. If an evidence-based retry is needed, preserve the first transcript and record why the retry was made.

Keep the author description and spoken transcript as separate source sections. The description expresses author framing; the transcript may contain different operational details. Neither independently verifies the author’s claims.

## Image and text posts

`yt-dlp` reporting no video formats can mean that the URL refers to an image or text post. It is not proof of an extractor installation failure. Fetch the page using configured network limits and inspect structured metadata.

If the caption is only hashtags or a short title, identify the post images from page metadata. Download only the images needed to understand substantive content, check their MIME type and size, then use an available OCR or vision capability.

For each image, preserve:

- image ordinal and original URL when permitted;
- verbatim OCR output;
- uncertain text, unreadable regions, and image-only claims;
- whether the image was actually inspected.

Never report engagement counts, author names, or image text unless they were directly recovered. Rendered UI counters and image captions may be inaccessible or unreliable.

## Completion criteria

- A video is complete only when media duration and usable transcript coverage meet the configured threshold.
- An image post is complete only when all substantive images have been inspected or the missed images are disclosed.
- A metadata preview is a valid partial result; label it as such rather than fabricating a full extraction.
