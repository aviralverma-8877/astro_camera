"""Logging configuration for Astro Camera"""
import logging
import logging.handlers
import os


def setup_logging(log_dir="/var/log/astro_camera", level=logging.INFO):
    """
    Configure logging for the application

    Args:
        log_dir: Directory for log files
        level: Logging level (default: INFO)

    Returns:
        Root logger instance
    """
    # Create log directory (if it doesn't exist and we have permissions)
    try:
        os.makedirs(log_dir, exist_ok=True)
        log_file_enabled = True
    except (OSError, PermissionError):
        # Fall back to console-only logging if we can't create log dir
        log_file_enabled = False
        print(f"Warning: Cannot create log directory {log_dir}, using console logging only")

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    simple_formatter = logging.Formatter('%(levelname)s: %(message)s')

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear any existing handlers
    root_logger.handlers.clear()

    # File handler (rotating, 10MB max, keep 7 files)
    if log_file_enabled:
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                os.path.join(log_dir, 'astro_camera.log'),
                maxBytes=10*1024*1024,  # 10MB
                backupCount=7
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(detailed_formatter)
            root_logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Cannot create log file: {e}")

    # Console handler (less verbose for cleaner output)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    root_logger.addHandler(console_handler)

    return root_logger
