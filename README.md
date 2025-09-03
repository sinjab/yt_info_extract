# YouTube Video Information Extractor

[![CI](https://github.com/sinjab/yt_info_extract/workflows/CI/badge.svg)](https://github.com/sinjab/yt_info_extract/actions)
[![PyPI version](https://badge.fury.io/py/yt-info-extract.svg)](https://badge.fury.io/py/yt-info-extract)
[![Python Support](https://img.shields.io/pypi/pyversions/yt-info-extract.svg)](https://pypi.org/project/yt-info-extract/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Coverage](https://codecov.io/gh/sinjab/yt_info_extract/branch/main/graph/badge.svg)](https://codecov.io/gh/sinjab/yt_info_extract)
[![Code Quality](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A robust Python library for extracting YouTube video metadata including title, description, channel name, publication date, and view count with multiple extraction strategies.

## Features

- **Multiple Extraction Strategies**: YouTube Data API v3 (official), yt-dlp, pytubefix
- **Automatic Fallback**: Seamlessly switches between methods if one fails
- **Flexible Input**: Support for video IDs and various YouTube URL formats
- **Batch Processing**: Extract information from multiple videos efficiently
- **Multiple Output Formats**: Text, JSON, CSV
- **Command Line Interface**: Easy-to-use CLI for quick extractions
- **Python Library**: Full programmatic access for integration
- **Robust Error Handling**: Graceful handling of failures with retry logic
- **Rate Limiting**: Built-in delays to respect YouTube's servers

## Installation

```bash
pip install yt-info-extract
```

### Optional Dependencies

For the best experience, install all extraction backends:

```bash
# For YouTube Data API v3 support (recommended)
pip install google-api-python-client

# For yt-dlp support (most robust fallback)
pip install yt-dlp

# For pytubefix support (lightweight fallback)
pip install pytubefix
```

## Quick Start

### Python Library Usage

```python
from yt_info_extract import get_video_info

# Extract video information
info = get_video_info("jNQXAC9IVRw")

print(f"Title: {info['title']}")
print(f"Channel: {info['channel_name']}")
print(f"Views: {info['views']:,}")
print(f"Published: {info['publication_date']}")
```

### Command Line Usage

```bash
# Extract video information
yt-info jNQXAC9IVRw

# Export to JSON
yt-info -f json -o video.json jNQXAC9IVRw

# Process multiple videos
yt-info --batch video_ids.txt --output-dir results/

# Use specific extraction strategy
yt-info -s api --api-key YOUR_KEY jNQXAC9IVRw
```

## YouTube Data API v3 Setup (Recommended)

The YouTube Data API v3 is the official, most reliable method. It requires a free API key:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create credentials (API Key)
5. Restrict the API key to YouTube Data API v3

```bash
# Set your API key as environment variable
export YOUTUBE_API_KEY="your_api_key_here"

# Now use the library
yt-info jNQXAC9IVRw
```

## Usage Examples

### Basic Usage

```python
from yt_info_extract import YouTubeVideoInfoExtractor

# Initialize extractor
extractor = YouTubeVideoInfoExtractor(api_key="your_key")

# Extract video info
info = extractor.get_video_info("jNQXAC9IVRw")

if info:
    print(f"Title: {info['title']}")
    print(f"Channel: {info['channel_name']}")
    print(f"Views: {info['views']:,}")
    print(f"Published: {info['publication_date']}")
    print(f"Description: {info['description'][:100]}...")
```

### Batch Processing

```python
from yt_info_extract import get_video_info_batch

video_ids = ["jNQXAC9IVRw", "dQw4w9WgXcQ", "_OBlgSz8sSM"]
results = get_video_info_batch(video_ids)

for result in results:
    if not result.get('error'):
        print(f"{result['title']} - {result['views']:,} views")
```

### Export Data

```python
from yt_info_extract import get_video_info, export_video_info

# Get video info
info = get_video_info("jNQXAC9IVRw")

# Export to JSON
export_video_info(info, "video.json")

# Export batch results to CSV
batch_results = get_video_info_batch(["jNQXAC9IVRw", "dQw4w9WgXcQ"])
export_video_info(batch_results, "videos.csv", format_type="csv")
```

### Different URL Formats

```python
from yt_info_extract import get_video_info

# All of these work:
formats = [
    "jNQXAC9IVRw",  # Video ID
    "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Standard URL
    "https://youtu.be/jNQXAC9IVRw",  # Short URL
    "https://www.youtube.com/embed/jNQXAC9IVRw",  # Embed URL
]

for fmt in formats:
    info = get_video_info(fmt)
    print(f"✓ {fmt} -> {info['title']}")
```

## Command Line Interface

### Basic Commands

```bash
# Extract video information
yt-info jNQXAC9IVRw

# Use different output formats
yt-info -f compact jNQXAC9IVRw
yt-info -f stats jNQXAC9IVRw
yt-info -f json jNQXAC9IVRw

# Export to file
yt-info -f json -o video.json jNQXAC9IVRw
yt-info -f csv -o video.csv jNQXAC9IVRw
```

### Batch Processing

```bash
# Create a file with video IDs (one per line)
echo "jNQXAC9IVRw" > video_ids.txt
echo "dQw4w9WgXcQ" >> video_ids.txt

# Process all videos
yt-info --batch video_ids.txt --output-dir results/

# With summary report
yt-info --batch video_ids.txt --summary --output-dir results/
```

### API Key Usage

```bash
# Method 1: Environment variable
export YOUTUBE_API_KEY="your_api_key_here"
yt-info jNQXAC9IVRw

# Method 2: Command line argument
yt-info --api-key "your_api_key_here" jNQXAC9IVRw

# Force specific strategy
yt-info -s api --api-key "your_key" jNQXAC9IVRw
yt-info -s yt_dlp jNQXAC9IVRw
```

### Utility Commands

```bash
# Test API key
yt-info --test-api

# List available strategies
yt-info --list-strategies

# Verbose output
yt-info -v jNQXAC9IVRw
```

## Extraction Strategies

### 1. YouTube Data API v3 (Recommended)

- **Pros**: Official, reliable, comprehensive data, compliant with ToS
- **Cons**: Requires API key, has quota limits (10,000 units/day free)
- **Best for**: Production applications, commercial use, reliable automation

```python
extractor = YouTubeVideoInfoExtractor(api_key="your_key", strategy="api")
```

### 2. yt-dlp (Most Robust Fallback)

- **Pros**: No API key needed, very robust, actively maintained
- **Cons**: Violates YouTube ToS, can break with YouTube updates
- **Best for**: Personal projects, research, when API quotas are insufficient

```python
extractor = YouTubeVideoInfoExtractor(strategy="yt_dlp")
```

### 3. pytubefix (Lightweight Fallback)

- **Pros**: No API key needed, simple, lightweight
- **Cons**: Violates YouTube ToS, less robust than yt-dlp
- **Best for**: Simple scripts, minimal dependencies

```python
extractor = YouTubeVideoInfoExtractor(strategy="pytubefix")
```

### 4. Auto Strategy (Default)

Automatically tries strategies in order of preference:
1. YouTube Data API v3 (if API key available)
2. yt-dlp (if installed)
3. pytubefix (if installed)

```python
extractor = YouTubeVideoInfoExtractor(strategy="auto")  # Default
```

## Data Structure

Each video information dictionary contains:

```python
{
    "title": "Video title",
    "description": "Full video description",
    "channel_name": "Channel name",
    "publication_date": "2005-04-23T00:00:00Z",  # ISO format
    "views": 123456789,  # Integer view count
    "extraction_method": "youtube_api"  # Method used
}
```

## Configuration Options

```python
extractor = YouTubeVideoInfoExtractor(
    api_key="your_key",           # YouTube Data API key
    strategy="auto",              # Extraction strategy
    timeout=30,                   # Request timeout (seconds)
    max_retries=3,                # Maximum retry attempts
    backoff_factor=0.75,          # Exponential backoff factor
    rate_limit_delay=0.1,         # Delay between requests
)
```

## Error Handling

The library handles errors gracefully:

```python
info = get_video_info("invalid_video_id")
if info:
    print(f"Success: {info['title']}")
else:
    print("Failed to extract video information")

# For batch processing, check individual results
results = get_video_info_batch(["valid_id", "invalid_id"])
for result in results:
    if result.get('error'):
        print(f"Error: {result['error']}")
    else:
        print(f"Success: {result['title']}")
```

## Legal and Compliance Notes

- **YouTube Data API v3**: Fully compliant with YouTube's Terms of Service
- **yt-dlp and pytubefix**: Violate YouTube's Terms of Service by scraping data

For commercial applications or production use, always use the YouTube Data API v3.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- Documentation: [GitHub README](https://github.com/sinjab/yt-info-extract)
- Issues: [GitHub Issues](https://github.com/sinjab/yt-info-extract/issues)
- API Key Setup: [Google Cloud Console](https://console.cloud.google.com/)

## Related Projects

- [yt-ts-extract](https://github.com/sinjab/yt-ts-extract) - YouTube transcript extraction
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader (used as fallback)
- [pytubefix](https://github.com/JuanBindez/pytubefix) - YouTube library (used as fallback)
