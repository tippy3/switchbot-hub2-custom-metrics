#!/usr/bin/env bash
set -eu

# Disable pagination
export AWS_PAGER=""

project="switchbot"
role_name="${project}-lambda-execution-role"
aws_account_id="$(aws sts get-caller-identity --query Account --output text)"

# Create IAM Role for Lambda

aws iam create-role \
  --role-name $role_name \
  --assume-role-policy-document file://aws/assume-role-policy.json

aws iam put-role-policy \
  --role-name $role_name \
  --policy-name $project \
  --policy-document file://aws/permission-policy.json

# Create CloudWatch Log Group

aws logs create-log-group \
  --log-group-name "/aws/lambda/${project}"

aws logs put-retention-policy \
  --log-group-name "/aws/lambda/${project}" \
  --retention-in-days 7

# Create Lambda Layer

aws lambda publish-layer-version \
  --layer-name $project \
  --zip-file fileb://layer.zip \
  --compatible-runtimes python3.11 \
  --compatible-architectures x86_64

layer_version="$(aws lambda list-layer-versions --layer-name $project --query 'LayerVersions[0].Version' --output text)"

# Create Lambda Function

aws lambda create-function \
  --function-name $project \
  --runtime python3.11 \
  --timeout 15 \
  --memory-size 256 \
  --zip-file fileb://function.zip \
  --handler main.lambda_handler \
  --role "arn:aws:iam::${aws_account_id}:role/${role_name}" \
  --layers "arn:aws:lambda:ap-northeast-1:${aws_account_id}:layer:${project}:${layer_version}"

aws lambda add-permission \
  --function-name $project \
  --statement-id events \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn "arn:aws:events:ap-northeast-1:${aws_account_id}:rule/${project}"

# Create Event Rule as Lambda Trigger

aws events put-rule \
  --name $project \
  --schedule-expression "cron(0/5 * * * ? *)"

aws events put-targets \
  --rule $project \
  --targets "Id=${project},Arn=arn:aws:lambda:ap-northeast-1:${aws_account_id}:function:${project}"
