#!/usr/bin/env bash
set +e
set -u

# Disable pagination
export AWS_PAGER=""

project="switchbot"
role_name="${project}-lambda-execution-role"

aws events remove-targets \
  --rule $project \
  --ids $project

aws events delete-rule \
  --name $project

aws lambda delete-function \
  --function-name $project

layer_version="$(aws lambda list-layer-versions --layer-name $project --query 'LayerVersions[0].Version' --output text)"

aws lambda delete-layer-version \
  --layer-name $project \
  --version-number $layer_version

aws logs delete-log-group \
  --log-group-name "/aws/lambda/${project}"

aws iam delete-role-policy \
  --role-name $role_name \
  --policy-name $project

aws iam delete-role \
  --role-name $role_name
