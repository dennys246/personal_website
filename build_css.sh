#!/usr/bin/env bash
# Build static/site.css with the Tailwind standalone CLI (no Node needed).
# Run after changing classes in templates/, and commit the result. Render also
# runs this at deploy, falling back to the committed file if it fails.
set -euo pipefail
cd "$(dirname "$0")"
VERSION=v3.4.17
case "$(uname -s)-$(uname -m)" in
  Darwin-arm64) ASSET=tailwindcss-macos-arm64 ;;
  Darwin-x86_64) ASSET=tailwindcss-macos-x64 ;;
  Linux-aarch64) ASSET=tailwindcss-linux-arm64 ;;
  *) ASSET=tailwindcss-linux-x64 ;;
esac
BIN=".tailwind/$ASSET-$VERSION"
if [ ! -x "$BIN" ]; then
  mkdir -p .tailwind
  curl -sSfL -o "$BIN" "https://github.com/tailwindlabs/tailwindcss/releases/download/$VERSION/$ASSET"
  chmod +x "$BIN"
fi
"$BIN" -c tailwind.config.js -i static/src/site.css -o static/site.css --minify
