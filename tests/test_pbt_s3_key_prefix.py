"""Property-based tests for S3 key prefix feature."""
import os
import unittest

from hypothesis import given, settings
from hypothesis import strategies as st

from src.app import build_key

# Environment variables cannot contain null bytes (OS-level constraint).
# Use a text strategy that excludes the null character.
env_safe_text = st.text(alphabet=st.characters(blacklist_characters="\x00"))


class TestBuildKeyProperties(unittest.TestCase):
    """Property-based tests for build_key."""

    @given(prefix=env_safe_text, suffix=st.text())
    @settings(max_examples=100)
    def test_property_1_build_key_concatenation(self, prefix: str, suffix: str):
        """
        Feature: s3-key-prefix, Property 1: build_key concatenation

        For any prefix and suffix, build_key(suffix) returns prefix + suffix
        when KEY_PREFIX is set to prefix.

        Validates: Requirements 1.3, 2.1, 3.1, 4.1, 5.1
        """
        os.environ["KEY_PREFIX"] = prefix
        try:
            result = build_key(suffix)
            assert result == prefix + suffix, (
                f"Expected '{prefix + suffix}', got '{result}'"
            )
        finally:
            del os.environ["KEY_PREFIX"]

    @given(prefix=env_safe_text, artist=st.text(), track=st.text())
    @settings(max_examples=100)
    def test_property_2_all_key_types_prefixed(self, prefix: str, artist: str, track: str):
        """
        Feature: s3-key-prefix, Property 2: All key types are correctly prefixed

        For any prefix, artist, and track, all three key types are correctly
        prefixed with KEY_PREFIX.

        Validates: Requirements 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 5.1
        """
        os.environ["KEY_PREFIX"] = prefix
        try:
            cover_key = build_key(f"{artist}/{track}/cover.png")
            assert cover_key == f"{prefix}{artist}/{track}/cover.png", (
                f"Cover key: expected '{prefix}{artist}/{track}/cover.png', got '{cover_key}'"
            )

            info_key = build_key(f"{artist}/{track}/info.json")
            assert info_key == f"{prefix}{artist}/{track}/info.json", (
                f"Info key: expected '{prefix}{artist}/{track}/info.json', got '{info_key}'"
            )

            no_cover_key = build_key("no-cover-400x400.png")
            assert no_cover_key == f"{prefix}no-cover-400x400.png", (
                f"No-cover key: expected '{prefix}no-cover-400x400.png', got '{no_cover_key}'"
            )
        finally:
            del os.environ["KEY_PREFIX"]


if __name__ == "__main__":
    unittest.main()
