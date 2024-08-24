#!/bin/sh
set -e

GITHUB_SHA=$1

BACKEND_APPLICATION_UUID="v4gco84"
FRONTEND_APPLICATION_UUID="fg00g0g"

echo "Deploying Showbuddy n with GITHUB_SHA: $GITHUB_SHA"

curl --request PATCH \
  --url https://coolify.rmbldc.com/api/v1/applications/$BACKEND_APPLICATION_UUID \
  --header "Authorization: Bearer ${COOLIFY_API_TOKEN}" \
  --header 'Content-Type: application/json' \
  --data "{
  \"docker_registry_image_tag\": \"$GITHUB_SHA\"
}"

curl --request PATCH \
  --url https://coolify.rmbldc.com/api/v1/applications/$FRONTEND_APPLICATION_UUID \
  --header "Authorization: Bearer ${COOLIFY_API_TOKEN}" \
  --header 'Content-Type: application/json' \
  --data "{
  \"docker_registry_image_tag\": \"$GITHUB_SHA\"
}"

# DEPLOY
curl --request GET \
  --url https://coolify.rmbldc.com/api/v1/deploy?uuid=$BACKEND_APPLICATION_UUID \
  --header "Authorization: Bearer ${COOLIFY_API_TOKEN}"

# DEPLOY
curl --request GET \
  --url https://coolify.rmbldc.com/api/v1/deploy?uuid=$FRONTEND_APPLICATION_UUID \
  --header "Authorization: Bearer ${COOLIFY_API_TOKEN}"
