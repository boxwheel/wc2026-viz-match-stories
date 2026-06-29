#!/usr/bin/env bash
# Usage: put_upload.sh <upload_url> <content_type> <filename> <local_file>
set -euo pipefail
URL="$1"; CT="$2"; FN="$3"; F="$4"
curl -sS -X PUT "$URL" -H "Content-Type: $CT" -H "X-Flywheel-Artifact-Filename: $FN" --data-binary @"$F" -o /dev/null -w "%{http_code}\n"
