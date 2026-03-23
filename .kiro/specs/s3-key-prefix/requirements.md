# Requirements Document

## Introduction

Add a configurable S3 key prefix to all S3 key access in the Maxi80 backend Lambda application. This allows relocating all S3 objects (artwork images and cached LastFM data) under a common subprefix (e.g., `v1/`) without code changes, controlled via an environment variable. The prefix is initially empty to ensure backward compatibility and safe deployment.

## Glossary

- **Lambda_Function**: The Maxi80 backend AWS Lambda function defined in `template.yaml`, entry point `src/app.py`
- **S3_Key**: The object key used to store or retrieve objects from the S3 artwork bucket
- **KEY_PREFIX**: An environment variable whose value is prepended to all S3 keys; defaults to empty string
- **Cover_Image_Key**: The S3 key for a cached track cover image, pattern `{artist}/{track}/cover.png`
- **Info_Key**: The S3 key for cached LastFM JSON response data, pattern `{artist}/{track}/info.json`
- **No_Cover_Key**: The S3 key for the default placeholder image, value `no-cover-400x400.png`
- **SAM_Template**: The AWS SAM `template.yaml` file that defines the Lambda function and its environment variables

## Requirements

### Requirement 1: KEY_PREFIX Environment Variable Declaration

**User Story:** As a DevOps engineer, I want a KEY_PREFIX environment variable defined in the SAM template, so that I can control the S3 key prefix without redeploying code.

#### Acceptance Criteria

1. THE SAM_Template SHALL declare a KEY_PREFIX environment variable under the Lambda_Function environment variables section
2. THE SAM_Template SHALL set the default value of KEY_PREFIX to an empty string
3. WHEN the Lambda_Function starts, THE Lambda_Function SHALL read the KEY_PREFIX value from the KEY_PREFIX environment variable

### Requirement 2: Prefix Applied to Cover Image Key

**User Story:** As a developer, I want the KEY_PREFIX prepended to cover image S3 keys, so that cover images can be stored under a configurable subprefix.

#### Acceptance Criteria

1. WHEN the Lambda_Function constructs a Cover_Image_Key, THE Lambda_Function SHALL prepend the KEY_PREFIX value to the Cover_Image_Key
2. WHEN KEY_PREFIX is an empty string, THE Lambda_Function SHALL produce a Cover_Image_Key identical to the current format `{artist}/{track}/cover.png`
3. WHEN KEY_PREFIX is set to a non-empty value (e.g., `v1/`), THE Lambda_Function SHALL produce a Cover_Image_Key in the format `{KEY_PREFIX}{artist}/{track}/cover.png`

### Requirement 3: Prefix Applied to Info Key

**User Story:** As a developer, I want the KEY_PREFIX prepended to info.json S3 keys, so that cached LastFM data can be stored under a configurable subprefix.

#### Acceptance Criteria

1. WHEN the Lambda_Function constructs an Info_Key, THE Lambda_Function SHALL prepend the KEY_PREFIX value to the Info_Key
2. WHEN KEY_PREFIX is an empty string, THE Lambda_Function SHALL produce an Info_Key identical to the current format `{artist}/{track}/info.json`
3. WHEN KEY_PREFIX is set to a non-empty value (e.g., `v1/`), THE Lambda_Function SHALL produce an Info_Key in the format `{KEY_PREFIX}{artist}/{track}/info.json`

### Requirement 4: Prefix Applied to No-Cover Placeholder Key

**User Story:** As a developer, I want the KEY_PREFIX prepended to the no-cover placeholder image key, so that the placeholder image can also be stored under the configurable subprefix.

#### Acceptance Criteria

1. WHEN the Lambda_Function constructs a No_Cover_Key, THE Lambda_Function SHALL prepend the KEY_PREFIX value to the No_Cover_Key
2. WHEN KEY_PREFIX is an empty string, THE Lambda_Function SHALL produce a No_Cover_Key identical to the current value `no-cover-400x400.png`
3. WHEN KEY_PREFIX is set to a non-empty value (e.g., `v1/`), THE Lambda_Function SHALL produce a No_Cover_Key in the format `{KEY_PREFIX}no-cover-400x400.png`

### Requirement 5: Backward Compatibility with Empty Prefix

**User Story:** As a DevOps engineer, I want the initial deployment with an empty KEY_PREFIX to produce identical S3 keys as the current implementation, so that I can verify nothing is broken before migrating objects.

#### Acceptance Criteria

1. WHEN KEY_PREFIX is an empty string, THE Lambda_Function SHALL access the same S3 keys as the current implementation without KEY_PREFIX
2. WHEN KEY_PREFIX is an empty string, THE Lambda_Function SHALL return identical response bodies for artwork requests compared to the current implementation

### Requirement 6: Verification Test for Prefix Behavior

**User Story:** As a developer, I want a Python test that verifies the downloaded info is the same before and after adding the KEY_PREFIX feature, so that I can confirm backward compatibility.

#### Acceptance Criteria

1. THE test suite SHALL include a test that verifies artwork request responses are identical when KEY_PREFIX is an empty string compared to when KEY_PREFIX is not set
2. THE test suite SHALL include a test that verifies S3 keys are correctly prefixed when KEY_PREFIX is set to a non-empty value
3. THE test suite SHALL verify that all three key types (Cover_Image_Key, Info_Key, No_Cover_Key) are correctly prefixed
