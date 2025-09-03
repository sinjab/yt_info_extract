# CLAUDE.md - AI Development Assistant Documentation

This document provides context for AI assistants working with the `yt_info_extract` project.

## Project Overview

`yt_info_extract` is a Python library for extracting YouTube video metadata (title, description, channel name, publication date, views) with multiple extraction strategies. It follows the architectural patterns established in the sister project `yt_ts_extract`.

## Project Status

**Published**: Available on PyPI as `yt-info-extract` v1.1.0  
**CI/CD**: Simplified GitHub Actions workflows for reliable testing and deployment  
**Test Coverage**: 95% comprehensive test coverage with unit and E2E tests  
**Installation**: `pip install yt-info-extract`

### Recent Breaking Changes (v1.1.0)

**BREAKING CHANGE**: As of v1.1.0, the library **only accepts YouTube video IDs** and no longer processes URLs.

- **Removed**: All URL parsing and validation capabilities
- **Changed**: `_extract_video_id()` → `_validate_video_id()` for strict ID validation
- **Input Format**: Only 11-character video IDs (A-Z, a-z, 0-9, _, -) are accepted
- **Error Handling**: URLs now return clear error messages instead of being processed
- **Migration**: Users must extract video IDs manually from URLs if needed

## Technical Architecture

### Core Design Principles

1. **Multi-Strategy Extraction**: Primary (YouTube Data API v3) with intelligent fallbacks (yt-dlp, pytubefix)
2. **Graceful Degradation**: Automatic strategy switching when methods fail
3. **Video ID Only Processing**: Strict validation of 11-character YouTube video IDs
4. **Rate Limiting**: Respectful of YouTube's servers with configurable delays
5. **Comprehensive Error Handling**: Robust retry logic with exponential backoff
6. **Multiple Interfaces**: Library API, CLI tool, and convenience functions

### Key Components

- **`extractor.py`**: Core extraction logic with strategy pattern implementation
- **`utils.py`**: Data formatting, validation, and export utilities
- **`cli.py`**: Command-line interface with comprehensive argument handling
- **`__init__.py`**: Public API with convenience functions

### Extraction Strategies

1. **YouTube Data API v3** (`strategy="api"`)
   - Official Google API requiring authentication
   - Quota-limited but highly reliable
   - Fully compliant with YouTube Terms of Service
   - Preferred for production applications

2. **yt-dlp** (`strategy="yt_dlp"`)
   - Community-maintained scraping tool
   - Most robust unofficial method
   - No API key required
   - Violates YouTube ToS but widely used

3. **pytubefix** (`strategy="pytubefix"`)
   - Lightweight scraping library
   - Simple interface with basic functionality
   - Less robust than yt-dlp
   - Also violates YouTube ToS

## Development Context

### Design Decisions Made

- **Strategy Pattern**: Allows seamless switching between extraction methods
- **Fail-Fast Validation**: Input validation occurs early in the pipeline
- **Structured Error Handling**: Consistent error format across all strategies
- **Rate Limiting**: Built-in delays prevent IP blocking and respect servers
- **Batch Optimization**: API requests can handle up to 50 video IDs efficiently

### Code Quality Standards

- **Type Hints**: Used throughout for better IDE support and documentation
- **Logging**: Comprehensive logging with appropriate levels
- **Docstrings**: All public methods have detailed docstrings
- **Error Messages**: Informative error messages for debugging
- **Resource Management**: Proper cleanup and context managers

## Common Development Tasks

### Adding New Extraction Methods

1. Add availability check in `__init__` method
2. Implement `_get_video_info_<method>` private method
3. Add method to strategy switching logic in `get_video_info`
4. Update `get_available_strategies` method
5. Add corresponding tests

### Extending Data Fields

1. Update return dictionary structure in extraction methods
2. Modify utility functions (formatting, validation) as needed
3. Update CLI output formats
4. Adjust export functions if new fields affect serialization
5. Update documentation and examples

### Performance Optimization

Current bottlenecks and considerations:
- Network requests are the primary latency source
- Batch processing significantly improves API efficiency
- Rate limiting balances performance with server respect
- Caching could be added for repeated requests

## Testing Strategy

### Test Suite Overview

**Coverage**: 94% comprehensive test coverage  
**Test Files**: 7 test modules covering all functionality  
**Test Count**: ~150+ individual test cases  
**CI/CD**: Automated testing on Python 3.9, 3.11, 3.12

### Test Categories

1. **Unit Tests** (`test_extractor.py`, `test_utils.py`, `test_cli.py`): Individual function testing with mocks
2. **End-to-End Tests** (`test_e2e.py`): Real API calls with stable test videos
3. **Coverage Gap Tests** (`test_coverage_gaps.py`): Edge cases and error scenarios
4. **Integration Tests** (`test_init.py`): Convenience function testing
5. **CLI Tests**: Command-line interface validation

### Testing Workflow

**Local Testing**: `uv run pytest tests/`  
**Coverage Report**: `uv run pytest --cov=yt_info_extract --cov-report=html`  
**CI Testing**: Simplified GitHub Actions workflow with essential checks  
**E2E Testing**: Uses stable YouTube videos with known metadata

### Testing Considerations

- E2E tests use stable test videos with predictable content
- Bot detection handling in CI environments
- Mock external dependencies for consistent unit testing
- Comprehensive error path coverage
- Strategy-specific testing for each extraction method

## Security Considerations

### API Key Management

- Environment variables preferred over hardcoded keys
- API key validation before use
- Clear error messages for authentication failures
- No API keys in logs or error messages

### Data Handling

- No sensitive data stored or logged
- Strict video ID validation to prevent injection
- Rate limiting to prevent abuse
- Graceful handling of malformed responses

## CLI Interface Design

The CLI follows Unix conventions:
- Short and long option forms (`-f` and `--format`)
- Meaningful error codes and messages
- Comprehensive help text with examples
- Batch processing support
- Multiple output formats

## Dependencies and Compatibility

### Core Dependencies
- `requests`: HTTP client for API calls
- `google-api-python-client`: Official YouTube API client

### Optional Dependencies
- `yt-dlp`: Robust fallback extraction
- `pytubefix`: Lightweight fallback extraction

### Python Compatibility
- Supports Python 3.8+ for broad compatibility
- Uses modern features while maintaining backward compatibility

## Performance Characteristics

### Typical Response Times
- API method: ~200-500ms per request
- yt-dlp method: ~1-3 seconds per request
- pytubefix method: ~500ms-2 seconds per request

### Scalability Considerations
- API quota limits daily usage (10,000 units default)
- Batch processing improves throughput significantly
- Rate limiting prevents server overload
- Memory usage scales linearly with batch size

## Troubleshooting Common Issues

### API Key Problems
- Invalid key format
- Quota exceeded
- API not enabled
- Insufficient permissions

### Network Issues
- Connection timeouts
- DNS resolution failures
- Proxy configuration problems
- Rate limiting triggered

### Strategy Failures
- Missing dependencies
- YouTube page structure changes
- Video access restrictions
- Geographic blocking

## Integration Patterns

### Library Usage
```python
# Quick extraction
info = get_video_info("video_id")

# Batch processing
results = get_video_info_batch(video_list)

# Custom configuration
extractor = YouTubeVideoInfoExtractor(
    strategy="api",
    timeout=60,
    max_retries=5
)
```

### CLI Integration
```bash
# Basic usage
yt-info video_id

# Batch with export
yt-info --batch ids.txt --output-dir results/

# API-specific usage
yt-info --api-key $KEY --strategy api video_id
```

## Future Enhancement Opportunities

### Potential Improvements
1. **Caching Layer**: Redis/database caching for repeated requests
2. **Concurrent Processing**: Async/threading for batch operations
3. **Additional Formats**: XML, YAML export options
4. **Metrics Collection**: Usage statistics and performance monitoring
5. **Configuration Files**: YAML/JSON config file support

### Architectural Considerations
- Plugin system for custom extraction methods
- Event hooks for monitoring and logging
- Configuration validation and schema
- Backward compatibility maintenance

## Related Projects

- **yt_ts_extract**: Sister project for transcript extraction
- **yt-dlp**: Upstream dependency for fallback extraction
- **google-api-python-client**: Official Google API client

## CI/CD and DevOps

### GitHub Actions Workflows

**Simplified Architecture**: After initial complex multi-job pipelines, workflows were simplified for reliability

#### CI Workflow (`.github/workflows/ci.yml`)
- **Trigger**: Push to main, pull requests
- **Python Versions**: 3.9, 3.11, 3.12
- **Jobs**: Test and build package
- **Features**: Code formatting checks (Black, isort), test execution, package building

#### Release Workflow (`.github/workflows/release.yml`)
- **Trigger**: New tags matching `v*.*.*`
- **Platform**: Ubuntu latest
- **Features**: Automated PyPI publishing via API token
- **Security**: Uses GitHub Secrets for secure PyPI authentication

### Development Commands

```bash
# Install dependencies
uv sync

# Run tests locally
uv run pytest tests/

# Code formatting
uv run black yt_info_extract tests
uv run isort yt_info_extract tests

# Coverage report
uv run pytest --cov=yt_info_extract --cov-report=html

# Build package
uv run python -m build
```

### Package Publishing

**PyPI Package**: `yt-info-extract`  
**Publishing Method**: GitHub Actions trusted publishing (secure, keyless)  
**Version Management**: Git tags trigger automated releases  
**Package Structure**: Modern pyproject.toml configuration

### Workflow Evolution

The project evolved from complex multi-platform CI/CD to simplified, reliable workflows:
- **Before**: 9-job complex pipeline with cross-platform testing, CodeQL, excessive security scanning
- **After**: Streamlined essential testing and publishing
- **Reason**: User feedback - "some failed some worked. lets make it simpler"
- **Result**: More reliable CI/CD with focus on core functionality

## Development History

### Major Milestones

1. **Initial Development**: Core extraction logic with multi-strategy architecture
2. **Testing Implementation**: Comprehensive test suite achieving 94% coverage
3. **CLI Development**: Full command-line interface with batch processing
4. **PyPI Publication**: Official package publication as `yt-info-extract`
5. **CI/CD Optimization**: Workflow simplification for reliability
6. **Production Ready**: Stable v1.0.0 release with comprehensive documentation
7. **API Simplification**: v1.1.0 breaking change to remove URL processing complexity

### Lessons Learned

- **YouTube Bot Detection**: CI environments often trigger bot detection, requiring test adaptations
- **Workflow Complexity**: Overly complex CI/CD pipelines reduce reliability
- **Cross-Platform Testing**: Not always necessary for Python libraries with standard dependencies
- **Code Formatting**: Essential for maintaining code quality in collaborative development
- **API Simplicity**: Removing complex URL processing improved reliability and maintainability
- **Breaking Changes**: Clear versioning and documentation essential for user communication

This documentation should help AI assistants understand the project's architecture, design decisions, development history, and current production status when providing assistance with code modifications, debugging, or feature additions.
