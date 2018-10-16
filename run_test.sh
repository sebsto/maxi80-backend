#!/bin/bash
cp maxi80_backend/app.py maxi80_backend/build/
export LASTFM_API_KEY=$(grep LASTFM_API_KEY ./tests/env.json | cut -d '"' -f 4)
export BUCKET=$(grep BUCKET ./tests/env.json | cut -d '"' -f 4)
AWS_PROFILE=maxi80 python3 -m unittest tests/test_handler.py
