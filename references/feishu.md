# Feishu/Lark documents and Minutes

## Documents and wikis

Use the organization-approved document API or CLI with the user’s existing authorization. Fetch Markdown or another lossless text representation and record the document identifier and revision when the API exposes them.

Do not assume a particular command, application ID, scope, or identity mode. Check the installed CLI help and active authorization first. If the document cannot be retrieved, report the exact authorization or scope block; do not try alternate identities or request permissions without user confirmation.

Embedded-image URLs can be short-lived authorization URLs. Treat alt text as metadata, not pixel evidence. When an image contains material information, use an authorized media download path and inspect the actual image; otherwise disclose that the image was not independently verified.

## Minutes

Minutes are meeting records, not ordinary video downloads. Do not use a public-video downloader or local ASR unless the user specifically requests an authorized offline copy.

1. Fetch metadata through the authorized Minutes API/CLI.
2. Normalize the documented duration field to integer seconds before writing frontmatter. Verify the actual response schema on the installed client; some clients expose a millisecond value under a nested `minute` object.
3. Fetch the transcript and AI summary only when the current authorization allows it.
4. Preserve the transcript verbatim with source-provided speaker labels and timestamps. Never infer a speaker’s real identity.

Avoid global CLI configuration changes. If an integration requires switching identity or authorization mode and cannot do so per command, show the exact change, obtain confirmation, capture the previous state, and restore it after the run.

For long meetings, archive the complete transcript locally and send a structured index or summary only when requested. Do not claim that a transport-limited card contains the entire transcript.

## Reuse and freshness

Before fetching again, search the configured archive by canonical URL and platform ID. Reuse a complete archive unless the user requests a refresh. A reused artifact must be reported as reused, with its prior capture date and any known limitations.
