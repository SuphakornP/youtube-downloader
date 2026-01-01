#!/usr/bin/env python3
"""YouTube Video Downloader - CLI entry point."""

import argparse
import sys
from typing import Optional

from src.downloader import FormatType, YouTubeDownloader


def print_banner() -> None:
    """Print the application banner."""
    print("\n" + "=" * 40)
    print("   YouTube Video Downloader v1.0")
    print("=" * 40 + "\n")


def get_url_input() -> str:
    """Prompt user for YouTube URL."""
    while True:
        url = input("Enter YouTube URL: ").strip()
        if url:
            return url
        print("URL cannot be empty. Please try again.\n")


def display_video_info(downloader: YouTubeDownloader) -> bool:
    """
    Display video information.

    Returns:
        True if info was fetched successfully, False otherwise.
    """
    print("\nFetching video info...")

    info = downloader.get_video_info()
    if not info:
        return False

    print(f"\nVideo: {downloader.get_video_title()}")
    print(f"Duration: {downloader.get_video_duration()}")
    return True


def select_format() -> FormatType:
    """Prompt user to select download format."""
    print("\nSelect format:")
    print("  [1] MP4    - Video (converted, best quality)")
    print("  [2] Source - Video (original format)")
    print("  [3] MP3    - Audio (320kbps)")
    print("  [4] AAC    - Audio (256kbps)")

    format_map = {
        '1': FormatType.MP4,
        '2': FormatType.SOURCE,
        '3': FormatType.MP3,
        '4': FormatType.AAC,
    }

    while True:
        choice = input("\nYour choice (1-4): ").strip()
        if choice in format_map:
            return format_map[choice]
        print("Invalid choice. Please enter 1, 2, 3, or 4.")


def confirm_download() -> bool:
    """Ask user to confirm download."""
    while True:
        confirm = input("\nProceed with download? (y/n): ").strip().lower()
        if confirm in ('y', 'yes'):
            return True
        if confirm in ('n', 'no'):
            return False
        print("Please enter 'y' or 'n'.")


def parse_format(format_str: str) -> Optional[FormatType]:
    """Parse format string to FormatType."""
    format_map = {
        'mp4': FormatType.MP4,
        'source': FormatType.SOURCE,
        'mp3': FormatType.MP3,
        'aac': FormatType.AAC,
    }
    return format_map.get(format_str.lower())


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Download YouTube videos and audio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py
  python3 main.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
  python3 main.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --format mp4
  python3 main.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --format mp3 --output ./downloads
        """
    )

    parser.add_argument(
        '--url', '-u',
        type=str,
        help='YouTube video URL'
    )

    parser.add_argument(
        '--format', '-f',
        type=str,
        choices=['mp4', 'source', 'mp3', 'aac'],
        help='Output format (mp4, source, mp3, aac)'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        default='downloads',
        help='Output directory (default: downloads)'
    )

    return parser.parse_args()


def run_interactive(output_path: str) -> int:
    """
    Run in interactive mode.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    print_banner()

    url = get_url_input()
    downloader = YouTubeDownloader(url, output_path)

    if not downloader.validate_url():
        print("\n✗ Invalid YouTube URL. Please check and try again.")
        return 1

    if not display_video_info(downloader):
        print("\n✗ Could not fetch video information.")
        return 1

    format_type = select_format()

    if not confirm_download():
        print("\nDownload cancelled.")
        return 0

    format_label = "audio" if format_type in (FormatType.MP3, FormatType.AAC) else "video"
    print(f"\nDownloading {format_label}...")

    if downloader.download(format_type):
        print(f"\n✓ Download complete!")
        return 0
    else:
        return 1


def run_with_args(args: argparse.Namespace) -> int:
    """
    Run with command-line arguments.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    print_banner()

    downloader = YouTubeDownloader(args.url, args.output)

    if not downloader.validate_url():
        print("✗ Invalid YouTube URL. Please check and try again.")
        return 1

    if not display_video_info(downloader):
        print("✗ Could not fetch video information.")
        return 1

    if args.format:
        format_type = parse_format(args.format)
    else:
        format_type = select_format()
        if not confirm_download():
            print("\nDownload cancelled.")
            return 0

    format_label = "audio" if format_type in (FormatType.MP3, FormatType.AAC) else "video"
    print(f"\nDownloading {format_label}...")

    if downloader.download(format_type):
        print(f"\n✓ Download complete!")
        return 0
    else:
        return 1


def main() -> int:
    """Main entry point."""
    try:
        args = parse_arguments()

        if args.url:
            return run_with_args(args)
        else:
            return run_interactive(args.output)

    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
