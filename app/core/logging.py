import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    log_dir = os.path.abspath(log_dir)
    os.makedirs(log_dir, exist_ok=True)  # ✅ Ensure logs directory exists

    log_file = os.path.join(log_dir, 'app.log')

    file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, logging.StreamHandler()]
    )
