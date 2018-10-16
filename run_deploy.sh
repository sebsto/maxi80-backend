#!/bin/bash

export AWS_PROFILE=maxi80
export STACK_NAME=Maxi80Backend
export REGION=eu-west-1

#
# Deploy the lambda function (now handled automatically by Pipeline : Update change set and Execute Change Set)
#
aws cloudformation deploy                               \
    --profile $AWS_PROFILE                              \
    --region $REGION                                    \
    --template-file ./template-packaged.yaml            \
    --stack-name $STACK_NAME                            \
    --capabilities CAPABILITY_IAM


# add a resource API to the gateway 

# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Principal": {
#                 "AWS": "arn:aws:iam::743602823695:user/seb"
#             },
#             "Action": "execute-api:Invoke",
#             "Resource": "arn:aws:execute-api:region:743602823695:Maxi80Backend/Prod/GET/artwork"
#         }
#     ]
# }

# aws apigateway update-rest-api \
#     --rest-api-id api-id \
#     --patch-operations op=replace,path=/policy,value='{\"jsonEscapedPolicyDocument\"}'

# aws apigateway create-deployment \
#      --rest-api-id 1234123412 
#      --stage-name dev 
#      --description 'Second deployment to the dev stage'

# TODO : add AWS_IAM as authentication type