#!/bin/bash

# Run E2E tests for yt_info_extract
# These tests make real network calls to YouTube

echo "🚀 Running E2E Tests for yt_info_extract"
echo "========================================"
echo ""

# Check if API key is set
if [ -z "$YOUTUBE_API_KEY" ]; then
    echo "⚠️  Warning: YOUTUBE_API_KEY not set. API tests will be skipped."
    echo "   To run API tests, set: export YOUTUBE_API_KEY='your_key'"
    echo ""
fi

# Run different test groups
echo "📋 Test Groups Available:"
echo "  1. All E2E tests (slow, ~2-3 minutes)"
echo "  2. API strategy tests only"
echo "  3. yt-dlp strategy tests only"
echo "  4. CLI tests only"
echo "  5. Quick smoke test (fast, ~10 seconds)"
echo ""

# Default to quick smoke test
TEST_GROUP=${1:-5}

case $TEST_GROUP in
    1)
        echo "Running all E2E tests..."
        pytest tests/test_e2e.py -m e2e -v
        ;;
    2)
        echo "Running API strategy tests..."
        pytest tests/test_e2e.py::TestE2EAPIStrategy -m e2e -v
        ;;
    3)
        echo "Running yt-dlp strategy tests..."
        pytest tests/test_e2e.py::TestE2EYtDlpStrategy -m e2e -v
        ;;
    4)
        echo "Running CLI tests..."
        pytest tests/test_e2e.py::TestE2ECLI -m e2e -v
        ;;
    5)
        echo "Running quick smoke test..."
        pytest tests/test_e2e.py::TestE2EConvenienceFunctions::test_get_video_info_function \
               tests/test_e2e.py::TestE2EAutoStrategy::test_auto_strategy_selection \
               tests/test_e2e.py::TestE2ECLI::test_cli_single_video \
               -m e2e -v
        ;;
    *)
        echo "Invalid option. Please choose 1-5"
        exit 1
        ;;
esac

echo ""
echo "✅ E2E tests completed!"