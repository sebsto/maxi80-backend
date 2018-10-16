#!/bin/bash
cp maxi80_backend/app.py maxi80_backend/build/
# pip3 install -r requirements.txt -t maxi80_backend/build/
sam local invoke -e ./tests/event.json --env-vars ./tests/env.json