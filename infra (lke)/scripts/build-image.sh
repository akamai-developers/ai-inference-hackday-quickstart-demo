#!/usr/bin/env bash
set -euo pipefail

# Build and push the workshop workspace image.
# Requires: docker logged in to ghcr.io (echo $CR_PAT | docker login ghcr.io -u USER --password-stdin)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$(dirname "$SCRIPT_DIR")"
CONTEXT="${INFRA_DIR}/images/workspace"

REGISTRY="${REGISTRY:-ghcr.io/akamai-developers}"
IMAGE="${IMAGE:-ai-agents-workspace}"
TAG="${TAG:-latest}"
WORKSHOP_REPO="${WORKSHOP_REPO:-https://github.com/akamai-developers/ai-agents-workshop.git}"

# Resolve WORKSHOP_REF to a concrete commit SHA so Docker layer caching does
# not silently bake an outdated workshop into the image. Without this, a
# rebuild with WORKSHOP_REF=main reuses the cached `git clone` layer and ships
# whatever was at HEAD the first time you built — even after the workshop
# repo has moved.
WORKSHOP_REF="${WORKSHOP_REF:-main}"
WORKSHOP_SHA="$(git ls-remote "${WORKSHOP_REPO}" "${WORKSHOP_REF}" | awk '{print $1}' | head -n1)"
if [ -z "${WORKSHOP_SHA}" ]; then
    echo "ERROR: could not resolve ${WORKSHOP_REPO}#${WORKSHOP_REF} to a SHA" >&2
    exit 1
fi

FULL_TAG="${REGISTRY}/${IMAGE}:${TAG}"

echo "=== Building ${FULL_TAG} ==="
echo "    workshop repo: ${WORKSHOP_REPO}"
echo "    workshop ref:  ${WORKSHOP_REF}  →  ${WORKSHOP_SHA}"
echo ""

docker build \
    --build-arg "WORKSHOP_REPO=${WORKSHOP_REPO}" \
    --build-arg "WORKSHOP_REF=${WORKSHOP_SHA}" \
    --tag "${FULL_TAG}" \
    --platform linux/amd64 \
    "${CONTEXT}"

echo ""
echo "=== Pushing ${FULL_TAG} ==="
docker push "${FULL_TAG}"

echo ""
echo "=== Done. ==="
echo "Image: ${FULL_TAG}"
