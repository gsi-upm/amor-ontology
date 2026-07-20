#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"

WIDOCO_VERSION="1.4.25"
WIDOCO_IMAGE="ghcr.io/dgarijo/widoco@sha256:ef0548a0522d26cc73f3c3ecdb265cbed59aab9eeaa51f18a6096acbc239a41c"

SOURCES=(
  "src/amor/amor.ttl"
  "src/bhv/bhv.ttl"
  "src/mft/mft.ttl"
  "src/amor/models/bhv/amor-bhv.ttl"
  "src/amor/models/mft/amor-mft.ttl"
  "src/amor/examples/amor-examples.ttl"
)
CONFIGS=(
  "in/amor/widoco-amor-config.properties"
  "in/bhv/widoco-bhv-config.properties"
  "in/mft/widoco-mft-config.properties"
  "in/amor/models/bhv/widoco-amor-bhv-config.properties"
  "in/amor/models/mft/widoco-amor-mft-config.properties"
  "in/amor/examples/widoco-amor-examples-config.properties"
)
INPUTS=(
  "in/amor/amor.ttl"
  "in/bhv/bhv.ttl"
  "in/mft/mft.ttl"
  "in/amor/models/bhv/amor-bhv.ttl"
  "in/amor/models/mft/amor-mft.ttl"
  "in/amor/examples/amor-examples.ttl"
)
OUTPUTS=(
  "out/amor/ns/doc"
  "out/bhv/ns/doc"
  "out/mft/ns/doc"
  "out/amor/models/bhv/ns/doc"
  "out/amor/models/mft/ns/doc"
  "out/amor/examples/doc"
)

if [[ "${1:-}" != "--allow-dirty" ]]; then
  if ! git diff --quiet HEAD -- "${SOURCES[@]}"; then
    echo "Normative sources differ from HEAD. Commit them before release generation." >&2
    exit 1
  fi
  SOURCE_STATE="clean"
else
  SOURCE_STATE="uncommitted"
fi

for index in "${!SOURCES[@]}"; do
  docker run --rm \
    -v "$ROOT/src:/usr/local/widoco/in:ro,Z" \
    -v "$ROOT/doc/ontologies:/usr/local/widoco/out:Z" \
    "$WIDOCO_IMAGE" \
    -confFile "${CONFIGS[$index]}" \
    -ontFile "${INPUTS[$index]}" \
    -outFolder "${OUTPUTS[$index]}" \
    -webVowl -rewriteAll
done

GENERATED_TURTLE=()
for output in "${OUTPUTS[@]}"; do
  GENERATED_TURTLE+=("doc/ontologies/${output#out/}/ontology.ttl")
done
UV_CACHE_DIR="${UV_CACHE_DIR:-/tmp/uv-cache}" \
  uv run --offline --frozen python scripts/repair_widoco_turtle.py "${GENERATED_TURTLE[@]}"

sha256sum "${SOURCES[@]}" > release/normative-artifacts.sha256
{
  printf 'source_commit=%s\n' "$(git rev-parse HEAD)"
  printf 'source_state=%s\n' "$SOURCE_STATE"
  printf 'widoco_version=%s\n' "$WIDOCO_VERSION"
  printf 'widoco_image=%s\n' "$WIDOCO_IMAGE"
} > doc/ontologies/BUILDINFO

echo "Generated documentation with WIDOCO $WIDOCO_VERSION from $(git rev-parse HEAD) ($SOURCE_STATE sources)."
