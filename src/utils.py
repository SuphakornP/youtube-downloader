"""Utility functions for the YouTube downloader."""

import re
import sys


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.

    Args:
        filename: The original filename.

    Returns:
        A sanitized filename safe for the filesystem.
    """
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    sanitized = sanitized.strip('. ')
    sanitized = re.sub(r'\s+', '_', sanitized)
    return sanitized[:200] if len(sanitized) > 200 else sanitized


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human-readable format.

    Args:
        seconds: Duration in seconds.

    Returns:
        Formatted duration string (e.g., "3:45" or "1:23:45").
    """
    if seconds is None:
        return "Unknown"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def format_size(bytes_size: int) -> str:
    """
    Format file size in bytes to human-readable format.

    Args:
        bytes_size: Size in bytes.

    Returns:
        Formatted size string (e.g., "45.2 MB").
    """
    if bytes_size is None:
        return "Unknown"

    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"


def print_progress_bar(
    percent: float,
    downloaded: str = "",
    speed: str = "",
    eta: str = "",
    width: int = 32
) -> None:
    """
    Print a progress bar to the console.

    Args:
        percent: Download percentage (0-100).
        downloaded: Downloaded size string.
        speed: Download speed string.
        eta: Estimated time remaining.
        width: Width of the progress bar.
    """
    filled = int(width * percent / 100)
    bar = '█' * filled + '░' * (width - filled)

    status_parts = []
    if downloaded:
        status_parts.append(downloaded)
    if speed:
        status_parts.append(speed)
    if eta:
        status_parts.append(f"ETA: {eta}")

    status = " - ".join(status_parts) if status_parts else ""

    sys.stdout.write(f"\r[{bar}] {percent:.1f}% {status}")
    sys.stdout.flush()
