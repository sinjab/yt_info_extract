#!/usr/bin/env python3
"""
Basic tests for YouTube Video Information Extractor
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from yt_info_extract import (
    YouTubeVideoInfoExtractor,
    get_video_info,
    get_video_stats,
    format_views,
    format_publication_date,
    clean_description,
)


class TestBasicFunctionality:
    """Test basic functionality without requiring network calls"""
    
    def test_video_id_extraction(self):
        """Test video ID extraction from various URL formats"""
        extractor = YouTubeVideoInfoExtractor()
        
        test_cases = [
            ("jNQXAC9IVRw", "jNQXAC9IVRw"),
            ("https://www.youtube.com/watch?v=jNQXAC9IVRw", "jNQXAC9IVRw"),
            ("https://youtu.be/jNQXAC9IVRw", "jNQXAC9IVRw"),
            ("https://www.youtube.com/embed/jNQXAC9IVRw", "jNQXAC9IVRw"),
            ("invalid", None),
            ("", None),
        ]
        
        for input_url, expected in test_cases:
            result = extractor._extract_video_id(input_url)
            assert result == expected, f"Failed for input: {input_url}"
    
    def test_format_views(self):
        """Test view count formatting"""
        test_cases = [
            (None, "Unknown views"),
            (0, "0 views"),
            (123, "123 views"),
            (1234, "1.2K views"),
            (1234567, "1.2M views"),
            (1234567890, "1.2B views"),
        ]
        
        for input_views, expected in test_cases:
            result = format_views(input_views)
            assert result == expected, f"Failed for input: {input_views}"
    
    def test_format_publication_date(self):
        """Test publication date formatting"""
        test_cases = [
            (None, "Unknown date"),
            ("", "Unknown date"),
            ("2005-04-23T00:00:00Z", "April 23, 2005"),
            ("2005-04-23", "April 23, 2005"),
        ]
        
        for input_date, expected in test_cases:
            result = format_publication_date(input_date)
            assert result == expected, f"Failed for input: {input_date}"
    
    def test_clean_description(self):
        """Test description cleaning"""
        test_cases = [
            (None, "No description available"),
            ("", "No description available"),
            ("Short description", "Short description"),
            ("A" * 600, "A" * 500 + "..."),
            ("Multiple\n\nlines\n\nof   text", "Multiple lines of text"),
        ]
        
        for input_desc, expected in test_cases:
            result = clean_description(input_desc)
            assert result == expected, f"Failed for input: {input_desc[:50]}..."
    
    def test_available_strategies(self):
        """Test strategy availability detection"""
        extractor = YouTubeVideoInfoExtractor()
        strategies = extractor.get_available_strategies()
        
        # Should return a list
        assert isinstance(strategies, list)
        
        # Should contain at least one strategy if dependencies are installed
        # This will vary based on the testing environment


class TestMockedExtraction:
    """Test extraction with mocked responses"""
    
    @patch('yt_info_extract.extractor.build')
    def test_api_extraction_success(self, mock_build):
        """Test successful API extraction with mocked response"""
        # Mock the YouTube service
        mock_service = MagicMock()
        mock_videos = MagicMock()
        mock_list = MagicMock()
        mock_request = MagicMock()
        
        mock_build.return_value = mock_service
        mock_service.videos.return_value = mock_videos
        mock_videos.list.return_value = mock_request
        
        # Mock API response
        mock_response = {
            "items": [{
                "snippet": {
                    "title": "Test Video",
                    "description": "Test description",
                    "channelTitle": "Test Channel",
                    "publishedAt": "2005-04-23T00:00:00Z"
                },
                "statistics": {
                    "viewCount": "1000000"
                }
            }]
        }
        mock_request.execute.return_value = mock_response
        
        # Test extraction
        extractor = YouTubeVideoInfoExtractor(api_key="test_key", strategy="api")
        result = extractor.get_video_info("jNQXAC9IVRw")
        
        assert result is not None
        assert result["title"] == "Test Video"
        assert result["description"] == "Test description"
        assert result["channel_name"] == "Test Channel"
        assert result["views"] == 1000000
        assert result["extraction_method"] == "youtube_api"
    
    @patch('yt_info_extract.extractor.build')
    def test_api_extraction_no_results(self, mock_build):
        """Test API extraction with no results"""
        mock_service = MagicMock()
        mock_videos = MagicMock()
        mock_list = MagicMock()
        mock_request = MagicMock()
        
        mock_build.return_value = mock_service
        mock_service.videos.return_value = mock_videos
        mock_videos.list.return_value = mock_request
        
        # Mock empty response
        mock_response = {"items": []}
        mock_request.execute.return_value = mock_response
        
        extractor = YouTubeVideoInfoExtractor(api_key="test_key", strategy="api")
        result = extractor.get_video_info("invalid_id")
        
        assert result is None


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_get_video_info_convenience_function(self):
        """Test the convenience function interface"""
        # This would require mocking the extractor
        # For now, just test that the function exists and handles invalid input
        result = get_video_info("invalid_video_id")
        # Should return None for invalid ID (no network call made)
        # The actual behavior depends on available strategies


class TestErrorHandling:
    """Test error handling scenarios"""
    
    def test_invalid_strategy(self):
        """Test initialization with invalid strategy"""
        with pytest.raises(ValueError):
            YouTubeVideoInfoExtractor(strategy="invalid_strategy")
    
    def test_missing_dependencies(self):
        """Test behavior when dependencies are missing"""
        with patch('yt_info_extract.extractor.YT_DLP_AVAILABLE', False):
            with pytest.raises(ImportError):
                YouTubeVideoInfoExtractor(strategy="yt_dlp")
        
        with patch('yt_info_extract.extractor.PYTUBEFIX_AVAILABLE', False):
            with pytest.raises(ImportError):
                YouTubeVideoInfoExtractor(strategy="pytubefix")


if __name__ == "__main__":
    # Simple test runner for development
    import sys
    
    # Run a few basic tests
    test_basic = TestBasicFunctionality()
    
    try:
        test_basic.test_video_id_extraction()
        print("✓ Video ID extraction test passed")
        
        test_basic.test_format_views()
        print("✓ View formatting test passed")
        
        test_basic.test_format_publication_date()
        print("✓ Date formatting test passed")
        
        test_basic.test_clean_description()
        print("✓ Description cleaning test passed")
        
        print("\nAll basic tests passed!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
