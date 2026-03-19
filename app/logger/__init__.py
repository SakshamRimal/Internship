import logging
import os

# Create directory for the common log file
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_filepath = os.path.join(log_dir, "app.log")

# 1. Initialize the logger with a specific name
logger = logging.getLogger("app_global")
logger.setLevel(logging.INFO)

# 2. Prevent logs from doubling up if this is imported multiple times
if not logger.handlers:
    # File Handler - All logs go here
    file_handler = logging.FileHandler(log_filepath)

    # Console Handler - So you can see it in the terminal too
    stream_handler = logging.StreamHandler()

    # Formatter - Includes the module name so you know WHERE the log came from
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)