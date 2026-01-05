# YouTube Downloader

A Python CLI tool for downloading YouTube videos and audio in multiple formats.

## Features

- **MP4** - Video download with best quality (converted)
- **Source** - Original video format (webm, mkv, etc.)
- **MP3** - Audio extraction at 320kbps
- **AAC** - Audio extraction at 256kbps

## Prerequisites

- Python 3.8+
- FFmpeg (required for format conversion)

```bash
# Install FFmpeg on macOS
brew install ffmpeg
```

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/youtube-downloader.git
cd youtube-downloader

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Interactive Mode

```bash
source .venv/bin/activate
python3 main.py
```

### Command Line Arguments

```bash
# Download as MP4
python3 main.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --format mp4

# Download as source format
python3 main.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --format source

# Download as MP3 audio
python3 main.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --format mp3

# Download as AAC audio
python3 main.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --format aac

# Specify custom output directory
python3 main.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --format mp4 --output ./my-videos
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--url` | `-u` | YouTube video URL |
| `--format` | `-f` | Output format: mp4, source, mp3, aac |
| `--output` | `-o` | Output directory (default: downloads) |
| `--browser` | `-b` | Browser to extract cookies from (chrome, firefox, safari, edge, opera, brave, chromium) |
| `--cookies` | `-c` | Path to cookies.txt file for authentication |

### Authentication (Avoid Rate Limits)

Use your YouTube account to avoid rate limiting:

```bash
# Use cookies from your browser (recommended)
python3 main.py --browser chrome
python3 main.py --browser firefox
python3 main.py --browser safari

# Or use a cookies.txt file
python3 main.py --cookies cookies.txt --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Supported browsers:** chrome, firefox, safari, edge, opera, brave, chromium

> **Note:** Make sure you're logged into YouTube in your browser before using the `--browser` option.

### Download Folder Structure

Files are automatically organized by format type:

```
downloads/
├── mp4/           # MP4 video files
├── source/        # Original format files
├── mp3/           # MP3 audio files
└── aac/           # AAC audio files
```

## Project Structure

```
youtube-downloader/
├── .venv/                 # Virtual environment (git ignored)
├── downloads/             # Downloaded files (git ignored)
│   ├── mp4/
│   ├── source/
│   ├── mp3/
│   └── aac/
├── docs/
│   └── PRD.md             # Product requirements
├── src/
│   ├── __init__.py
│   ├── downloader.py      # Core download logic
│   ├── validator.py       # URL validation
│   └── utils.py           # Helper functions
├── main.py                # CLI entry point
├── requirements.txt
├── README.md
└── LICENSE
```

## License

MIT License
