# Tasks

## Task 1: Add build_key helper function
- [x] 1.1 Add `build_key(suffix: str) -> str` function to `src/app.py` that reads `KEY_PREFIX` from `os.environ` (defaulting to `""`) and returns `prefix + suffix`

## Task 2: Update S3 key construction sites to use build_key
- [x] 2.1 Update `get_artwork_url()` in `src/app.py`: replace `NO_COVER_IMAGE` usage in `defaultImage()` with `build_key(NO_COVER_IMAGE)`
- [x] 2.2 Update `get_artwork_url()` in `src/app.py`: replace cover image key `"%s/%s/cover.png" % (artist, track)` with `build_key(f"{artist}/{track}/cover.png")`
- [x] 2.3 Update `artwork()` in `src/app.py`: replace info key `"%s/%s/info.json" % (ARTIST, TRACK)` with `build_key(f"{ARTIST}/{TRACK}/info.json")`

## Task 3: Add KEY_PREFIX to SAM template
- [x] 3.1 Add `KEY_PREFIX: ""` to the Environment Variables section of the `Maxi80Backend` function in `template.yaml`

## Task 4: Add hypothesis dependency
- [x] 4.1 Add `hypothesis` to test dependencies (e.g., `requirements.txt` or a test requirements file)

## Task 5: Add property-based tests
- [x] 5.1 Add property test for Property 1 (build_key concatenation): for random prefix and suffix, `build_key(suffix)` returns `prefix + suffix` — tag: `Feature: s3-key-prefix, Property 1: build_key concatenation` [PBT: Property 1]
- [x] 5.2 Add property test for Property 2 (all key types prefixed): for random prefix, artist, track, verify cover key, info key, and no-cover key are correctly prefixed — tag: `Feature: s3-key-prefix, Property 2: All key types are correctly prefixed` [PBT: Property 2]

## Task 6: Add unit tests for backward compatibility and prefix behavior
- [x] 6.1 Add unit test verifying that with `KEY_PREFIX=""`, the Lambda handler produces identical responses to the current implementation (Requirement 6.1)
- [x] 6.2 Add unit test verifying that with `KEY_PREFIX="v1/"`, S3 calls use keys starting with `v1/` for all three key types (Requirement 6.2, 6.3)
- [x] 6.3 Add unit test verifying that when `KEY_PREFIX` is not set in the environment, `build_key` defaults to empty string
