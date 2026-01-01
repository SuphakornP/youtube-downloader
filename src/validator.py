"""URL validation module for YouTube URLs."""

import re
from typing import Optional


class URLValidator:
    """Validates YouTube URLs and extracts video IDs."""

    YOUTUBE_PATTERNS = [
        r'^https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        r'^https?://(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]{11})',
        r'^https?://(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        r'^https?://(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})',
        r'^https?://youtu\.be/([a-zA-Z0-9_-]{11})',
        r'^https?://(?:www\.)?youtube\.com/live/([a-zA-Z0-9_-]{11})',
    ]

    @classmethod
    def validate(cls, url: str) -> bool:
        """
        Validate if the given URL is a valid YouTube URL.

        Args:
            url: The URL to validate.

        Returns:
            True if valid YouTube URL, False otherwise.
        """
        if not url:
            return False

        for pattern in cls.YOUTUBE_PATTERNS:
            if re.match(pattern, url):
                return True
        return False

    @classmethod
    def extract_video_id(cls, url: str) -> Optional[str]:
        """
        Extract the video ID from a YouTube URL.

        Args:
            url: The YouTube URL.

        Returns:
            The video ID if found, None otherwise.
        """
        if not url:
            return None

        for pattern in cls.YOUTUBE_PATTERNS:
            match = re.match(pattern, url)
            if match:
                return match.group(1)
        return None
