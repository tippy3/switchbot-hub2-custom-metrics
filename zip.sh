#!/usr/bin/env bash
set -eu

# Lambda Function
rm -f function.zip
zip -j function.zip app/*.py

# Lambda Layer
rm -rf python
pip install requests aws_secretsmanager_caching -t python
rm -f layer.zip
zip -r layer.zip python
