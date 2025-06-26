import os
import json
from pathlib import Path
import logging


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('video_automation.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def validate_config():
    """Validate configuration file and required settings"""
    config_path = Path(__file__).parent.parent / 'config' / 'config.json'

    if not config_path.exists():
        raise FileNotFoundError(
            "Configuration file not found. Please create config/config.json")

    with open(config_path) as f:
        config = json.load(f)

    # Check required API keys
    required_keys = [
        ('openrouter', 'api_key'),
        ('elevenlabs', 'api_key')
    ]

    for section, key in required_keys:
        if not config.get(section, {}).get(key):
            raise ValueError(
                f"Missing required configuration: {section}.{key}")

    return config


def check_ffmpeg():
    """Check if FFmpeg is available in the system"""
    try:
        import ffmpeg
        # Try to get FFmpeg version
        ffmpeg.probe('dummy', v='quiet')
    except ffmpeg.Error:
        # This is expected for dummy input, FFmpeg is available
        return True
    except FileNotFoundError:
        return False
    except Exception:
        return False

    return True


def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        'output',
        'assets',
        'config'
    ]

    base_path = Path(__file__).parent.parent

    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(exist_ok=True)


def clean_filename(filename):
    """Clean filename to be filesystem safe"""
    import re
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    return filename


def format_duration(seconds):
    """Format duration in seconds to human readable format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def get_file_size(file_path):
    """Get file size in human readable format"""
    size = os.path.getsize(file_path)

    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0

    return f"{size:.1f} TB"


class ProgressTracker:
    """Simple progress tracker for long operations"""

    def __init__(self, total_steps):
        self.total_steps = total_steps
        self.current_step = 0

    def update(self, step_name):
        self.current_step += 1
        percentage = (self.current_step / self.total_steps) * 100
        print(f"[{percentage:.1f}%] {step_name}")

    def complete(self):
        print("[100%] Process completed!")


if __name__ == "__main__":
    # Test utilities
    logger = setup_logging()
    logger.info("Testing utilities...")

    try:
        config = validate_config()
        logger.info("Configuration validated successfully")
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")

    if check_ffmpeg():
        logger.info("FFmpeg is available")
    else:
        logger.warning("FFmpeg not found - video processing may fail")

    ensure_directories()
    logger.info("Directories ensured")
