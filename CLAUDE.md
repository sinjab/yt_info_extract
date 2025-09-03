# CLAUDE.md - AI Development Assistant Documentation

This document provides context for AI assistants working with the `yt_info_extract` project.

## Project Overview

`yt_info_extract` is a Python library for extracting YouTube video metadata (title, description, channel name, publication date, views) with multiple extraction strategies.

**Current Status**: Available on PyPI as `yt-info-extract` v1.1.0 with 95% test coverage

### Recent Breaking Changes (v1.1.0)

**BREAKING CHANGE**: The library **only accepts YouTube video IDs** and no longer processes URLs.

- **Input Format**: Only 11-character video IDs (A-Z, a-z, 0-9, _, -) are accepted
- **Changed**: `_extract_video_id()` → `_validate_video_id()` for strict ID validation
- **Migration**: Users must extract video IDs manually from URLs if needed

## Technical Architecture

### Core Design Principles

1. **Multi-Strategy Extraction**: YouTube Data API v3 (primary) with intelligent fallbacks (yt-dlp, pytubefix)
2. **Video ID Only Processing**: Strict validation of 11-character YouTube video IDs
3. **Graceful Degradation**: Automatic strategy switching when methods fail
4. **Rate Limiting & Error Handling**: Robust retry logic with exponential backoff

### Key Components

- **`extractor.py`**: Core extraction logic with strategy pattern
- **`utils.py`**: Data formatting, validation, and export utilities
- **`cli.py`**: Command-line interface with batch processing
- **`__init__.py`**: Public API with convenience functions

### Extraction Strategies

1. **YouTube Data API v3** (`strategy="api"`) - Official, reliable, ToS compliant (requires API key)
2. **yt-dlp** (`strategy="yt_dlp"`) - Most robust fallback (violates YouTube ToS)
3. **pytubefix** (`strategy="pytubefix"`) - Lightweight fallback (violates YouTube ToS)

## Development Context

### Common Development Tasks

**Adding New Extraction Methods:**
1. Add availability check in `__init__` method
2. Implement `_get_video_info_<method>` private method
3. Update strategy switching logic and `get_available_strategies`
4. Add corresponding tests

**Extending Data Fields:**
1. Update return dictionary structure in extraction methods
2. Modify utility functions and CLI output formats
3. Update export functions and documentation

### Performance Characteristics

- **Response Times**: API ~200-500ms, yt-dlp ~1-3s, pytubefix ~500ms-2s
- **Bottlenecks**: Network requests are primary latency source
- **Optimization**: Batch processing significantly improves API efficiency
- **Scalability**: API quota limits (10,000 units/day), memory scales linearly

## Testing Strategy

**Coverage**: 95% across 7 test modules with ~150+ test cases

### Test Categories
1. **Unit Tests**: Individual function testing with mocks
2. **E2E Tests**: Real API calls with stable test videos  
3. **Integration Tests**: Convenience function testing
4. **CLI Tests**: Command-line interface validation

### Commands
```bash
uv run pytest tests/                                    # Run all tests
uv run pytest --cov=yt_info_extract --cov-report=html  # Coverage report
export YOUTUBE_API_KEY="key" && uv run pytest tests/test_e2e.py  # E2E with API
```

## Security & Best Practices

### API Key Management
- Environment variables preferred over hardcoded keys
- API key validation before use, no keys in logs
- Clear error messages for authentication failures

### Data Handling
- Strict video ID validation prevents injection attacks
- Rate limiting prevents abuse
- No sensitive data stored or logged

## CI/CD & Development

### GitHub Actions Workflows
- **CI**: Automated testing on Python 3.9, 3.11, 3.12 with code formatting checks
- **Release**: Tag-triggered PyPI publishing via GitHub Secrets

### Development Commands
```bash
uv sync                                        # Install dependencies
uv run black yt_info_extract tests           # Code formatting
uv run isort yt_info_extract tests           # Import sorting
uv run python -m build                       # Build package
```

## Integration Patterns

### Library Usage
```python
from yt_info_extract import get_video_info, YouTubeVideoInfoExtractor

# Quick extraction
info = get_video_info("jNQXAC9IVRw")

# Custom configuration
extractor = YouTubeVideoInfoExtractor(strategy="api", timeout=60)
```

### CLI Usage
```bash
yt-info jNQXAC9IVRw                          # Basic extraction
yt-info --batch ids.txt --output-dir results/ # Batch processing
yt-info -s api --api-key $KEY video_id        # API-specific
```

## Troubleshooting

### Common Issues
- **API Problems**: Invalid key, quota exceeded, API not enabled
- **Network Issues**: Timeouts, DNS failures, rate limiting
- **Strategy Failures**: Missing dependencies, YouTube structure changes

### Dependencies
- **Core**: `requests`, `google-api-python-client`  
- **Optional**: `yt-dlp`, `pytubefix`
- **Python**: 3.8+ supported

## Development History

### Major Milestones
1. **v1.0.0**: Initial production release with comprehensive documentation
2. **v1.1.0**: API simplification - removed URL processing complexity

### Key Lessons Learned
- **API Simplicity**: Removing complex URL processing improved reliability and maintainability
- **Workflow Simplicity**: Streamlined CI/CD over complex multi-job pipelines
- **Breaking Changes**: Clear versioning and documentation essential for user communication
- **YouTube Bot Detection**: CI environments require test adaptations

### Related Projects
- **yt_ts_extract**: Sister project for transcript extraction
- **yt-dlp**: Upstream dependency for fallback extraction

---

This documentation helps AI assistants understand the project's current architecture, recent breaking changes, and development context for effective assistance with code modifications and feature additions.