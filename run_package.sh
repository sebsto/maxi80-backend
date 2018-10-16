#!/bin/bash 

export AWS_PROFILE=maxi80
export S3_BUCKET=artwork.maxi80.com
export S3_PREFIX=deploy/sam
export REGION=eu-west-1

cp maxi80_backend/app.py maxi80_backend/build/

aws cloudformation package                      \
    --profile $AWS_PROFILE                      \
    --region $REGION                            \
    --template-file ./template.yaml         \
    --s3-bucket $S3_BUCKET                      \
    --s3-prefix $S3_PREFIX                      \
    --output-template-file ./template-packaged.yaml
