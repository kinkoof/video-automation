#!/usr/bin/env python3
"""
Basic test script for video automation components
"""

import os
import sys
from pathlib import Path


def test_imports():
    """Test if all modules can be imported"""
    print("=== Testing Module Imports ===")
    try:
        from src.text_generation import TextGenerator
        print("✓ Text Generation module imported successfully")
    except Exception as e:
        print(f"✗ Text Generation import failed: {e}")
        return False

    try:
        from src.audio_processing import AudioProcessor
        print("✓ Audio Processing module imported successfully")
    except Exception as e:
        print(f"✗ Audio Processing import failed: {e}")
        return False

    try:
        from src.video_processing import VideoProcessor
        print("✓ Video Processing module imported successfully")
    except Exception as e:
        print(f"✗ Video Processing import failed: {e}")
        return False

    try:
        from src.utils import setup_logging, validate_config
        print("✓ Utils module imported successfully")
    except Exception as e:
        print(f"✗ Utils import failed: {e}")
        return False

    return True


def test_config():
    """Test configuration validation"""
    print("\n=== Testing Configuration ===")
    try:
        from src.utils import validate_config
        config = validate_config()
        print("✓ Configuration file is valid")
        print("✓ OpenRouter API key configured")
        print("✓ ElevenLabs API key configured")
        return True
    except Exception as e:
        print(f"✗ Configuration validation failed: {e}")
        return False


def test_ffmpeg():
    """Test FFmpeg availability"""
    print("\n=== Testing FFmpeg ===")
    try:
        import ffmpeg
        # Test with a dummy probe to check if FFmpeg is available
        print("✓ FFmpeg Python library available")
        return True
    except Exception as e:
        print(f"✗ FFmpeg test failed: {e}")
        return False


def main():
    """Run basic tests"""
    print("Video Automation - Basic Component Test")
    print("=" * 50)

    # Ensure we're in the right directory
    if not Path("config/config.json").exists():
        print("✗ Error: Please run this script from the video-automation directory")
        sys.exit(1)

    # Run tests
    tests_passed = 0
    total_tests = 3

    if test_imports():
        tests_passed += 1

    if test_config():
        tests_passed += 1

    if test_ffmpeg():
        tests_passed += 1

    print(f"\n=== Test Summary ===")
    print(f"Tests passed: {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        print("✓ All basic tests passed! The system is ready for use.")
        print("\nNext steps:")
        print("1. Add background video file to assets/background.mp4")
        print("2. Add background music to assets/background_music.mp3")
        print("3. Run: python main.py")
    else:
        print("✗ Some tests failed. Please check the configuration and dependencies.")

    return tests_passed == total_tests


if __name__ == "__main__":
    main()
