#!/bin/bash
echo "Zipping code..."
/usr/bin/zip deployment.zip lambda_function.py
echo "Deploying to Lambda..."
aws --region ap-southeast-1 lambda update-function-code --zip-file fileb://deployment.zip --function-name checksite --publish
echo "Cleaning up..."
/bin/rm deployment.zip
