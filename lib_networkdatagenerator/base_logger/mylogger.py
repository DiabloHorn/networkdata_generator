"""Base logger
"""
import logging

gnd_logger = logging.getLogger("networkdata_generator")
if len(gnd_logger.handlers) == 0:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s::%(filename)s::%(funcName)s] %(message)s", "%Y-%m-%d %H:%M:%S"
        )
    )
    gnd_logger.addHandler(console_handler)
gnd_logger.setLevel(logging.ERROR)
