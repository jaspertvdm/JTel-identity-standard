#!/usr/bin/env bash
set -euo pipefail

# Simple end-to-end test against the JIS router.
# Usage:
#   BASE=http://localhost:18081 SECRET=changeme ./test.sh
# or override BASE with your LAN IP: BASE=http://<pi-ip>:18081

BASE="${BASE:-http://localhost:18081}"
SECRET="${SECRET:-changeme}"

echo "Using BASE=$BASE"

header() { echo; echo "== $* =="; }

header "Health"
curl -sf "$BASE/health" && echo

header "FIR/A init"
INIT=$(curl -s -X POST "$BASE/fira/init" \
  -H "X-JIS-SECRET: $SECRET" -H "Content-Type: application/json" \
  -d '{"initiator":"app-client","responder":"server-core","roles":["client","server"],"context":{"channel":"test"}}')
echo "$INIT"
FIR=$(echo "$INIT" | jq -r .fir_a_id)
HASH=$(echo "$INIT" | jq -r .continuity_hash)

header "IFT (intent)"
IFT=$(curl -s -X POST "$BASE/ift" \
  -H "X-JIS-SECRET: $SECRET" -H "Content-Type: application/json" \
  -d "{\"fir_a_id\":\"$FIR\",\"intent\":\"unlock_door\",\"context\":{\"humotica\":\"natural_language\"},\"continuity_hash_prev\":\"$HASH\"}")
echo "$IFT"
HASH=$(echo "$IFT" | jq -r .continuity_hash)

header "NIR notify (simulate doubt)"
NIR=$(curl -s -X POST "$BASE/nir/notify" \
  -H "X-JIS-SECRET: $SECRET" -H "Content-Type: application/json" \
  -d "{\"fir_a_id\":\"$FIR\",\"reason\":\"unusual_time\",\"continuity_hash_prev\":\"$HASH\"}")
echo "$NIR"
HASH=$(echo "$NIR" | jq -r .continuity_hash)

header "NIR confirm (rectify)"
CONF=$(curl -s -X POST "$BASE/nir/confirm" \
  -H "X-JIS-SECRET: $SECRET" -H "Content-Type: application/json" \
  -d "{\"fir_a_id\":\"$FIR\",\"method\":\"pin\",\"result\":\"confirmed\",\"continuity_hash_prev\":\"$HASH\"}")
echo "$CONF"

echo
echo "Done. Verify continuity_hash updates and no HTTP errors."
