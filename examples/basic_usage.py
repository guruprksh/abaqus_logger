"""Minimal example: writes example_log.txt into ./output."""
import os

from abaqus_logger import SimpleLogger

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

logger = SimpleLogger(model_name="Example", work_dir=out_dir, log_name="example")
logger.add_header("INITIALIZATION", pad=4)
logger.add("Init", "INFO", "Output directory: {}".format(out_dir))
logger.add_header("DATA LOADING", pad=4)
logger.add("Load", "SUCCESS", "Matched 120 nodes")
logger.add("Load", "WARNING", "Missing coords file: part_3.csv")
logger.add_separator()
logger.save()
