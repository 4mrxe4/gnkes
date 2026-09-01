# Plugins1/FinalMusic/fm_core/dir.py
from helpers.context import redis_proxy as r, dev_final_proxy as Dev_FINAL, k_proxy as k
from pathlib import Path
import logging
logger = logging.getLogger("FinalMusic")
def ensure_dirs():
    for dir in ["cache", "downloads"]:
        Path(dir).mkdir(parents=True, exist_ok=True)
    logger.info("📁 Cache directories updated.")