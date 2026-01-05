"""Core download logic for YouTube videos and audio."""

import os
import sys
from enum import Enum
from typing import Callable, Optional

import yt_dlp

from .utils import format_duration, format_size, print_progress_bar
from .validator import URLValidator


class FormatType(Enum):
    """Supported download format types."""

    MP4 = "mp4"
    SOURCE = "source"
    MP3 = "mp3"
    AAC = "aac"


SUPPORTED_BROWSERS = ['chrome', 'firefox', 'safari', 'edge', 'opera', 'brave', 'chromium']


class YouTubeDownloader:
    """Downloads YouTube videos and audio in various formats."""

    def __init__(self, url: str, output_path: str = ".", browser: Optional[str] = None, cookies_file: Optional[str] = None):
        """
        Initialize the downloader.

        Args:
            url: YouTube video URL.
            output_path: Directory to save downloaded files.
            browser: Browser name to extract cookies from (chrome, firefox, safari, edge, etc.).
            cookies_file: Path to cookies.txt file for authentication.
        """
        self.url = url
        self.output_path = output_path
        self.browser = browser
        self.cookies_file = cookies_file
        self._video_info: Optional[dict] = None

    def _get_auth_options(self) -> dict:
        """Get authentication options for yt-dlp."""
        auth_opts = {}
        if self.browser:
            auth_opts['cookiesfrombrowser'] = (self.browser,)
        elif self.cookies_file and os.path.exists(self.cookies_file):
            auth_opts['cookiefile'] = self.cookies_file
        return auth_opts

    def validate_url(self) -> bool:
        """
        Validate the YouTube URL.

        Returns:
            True if valid, False otherwise.
        """
        return URLValidator.validate(self.url)

    def get_video_info(self) -> Optional[dict]:
        """
        Fetch video metadata without downloading.

        Returns:
            Dictionary containing video info, or None on error.
        """
        if self._video_info:
            return self._video_info

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'extractor_retries': 5,
            'sleep_interval': 5,
            'max_sleep_interval': 30,
            'sleep_interval_requests': 1,
            **self._get_auth_options(),
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                self._video_info = ydl.sanitize_info(info)
                return self._video_info
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            if 'rate-limited' in error_msg.lower() or "isn't available" in error_msg.lower():
                print(f"\n⚠ YouTube rate limit detected. Please wait a few minutes and try again.")
            else:
                print(f"\nError fetching video info: {e}")
            return None

    def get_video_title(self) -> str:
        """Get the video title."""
        info = self.get_video_info()
        return info.get('title', 'Unknown') if info else 'Unknown'

    def get_video_duration(self) -> str:
        """Get formatted video duration."""
        info = self.get_video_info()
        if info:
            return format_duration(info.get('duration'))
        return 'Unknown'

    def _create_progress_hook(self) -> Callable:
        """Create a progress hook for download status updates."""

        def progress_hook(d: dict) -> None:
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)

                if total > 0:
                    percent = (downloaded / total) * 100
                else:
                    percent = 0

                speed = d.get('_speed_str', '')
                eta = d.get('_eta_str', '')
                downloaded_str = format_size(downloaded)

                print_progress_bar(percent, downloaded_str, speed, eta)

            elif d['status'] == 'finished':
                print("\n✓ Download finished, processing...")

            elif d['status'] == 'error':
                print("\n✗ Error occurred during download")

        return progress_hook

    def _get_ydl_options(self, format_type: FormatType) -> dict:
        """
        Get yt-dlp options for the specified format.

        Args:
            format_type: The desired output format.

        Returns:
            Dictionary of yt-dlp options.
        """
        format_folder = os.path.join(self.output_path, format_type.value)
        os.makedirs(format_folder, exist_ok=True)

        base_opts = {
            'outtmpl': f'{format_folder}/%(title)s.%(ext)s',
            'progress_hooks': [self._create_progress_hook()],
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'extractor_retries': 5,
            'retries': 10,
            'fragment_retries': 10,
            'sleep_interval': 5,
            'max_sleep_interval': 30,
            'sleep_interval_requests': 1,
            **self._get_auth_options(),
        }

        if format_type == FormatType.MP4:
            return {
                **base_opts,
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
            }

        elif format_type == FormatType.SOURCE:
            return {
                **base_opts,
                'format': 'bestvideo+bestaudio/best',
            }

        elif format_type == FormatType.MP3:
            return {
                **base_opts,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
            }

        elif format_type == FormatType.AAC:
            return {
                **base_opts,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'aac',
                    'preferredquality': '256',
                }],
            }

        raise ValueError(f"Unsupported format type: {format_type}")

    def download(self, format_type: FormatType) -> bool:
        """
        Download the video/audio in the specified format.

        Args:
            format_type: The desired output format.

        Returns:
            True if download succeeded, False otherwise.
        """
        ydl_opts = self._get_ydl_options(format_type)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            return True
        except yt_dlp.utils.DownloadError as e:
            print(f"\n✗ Download failed: {e}")
            return False
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            return False
