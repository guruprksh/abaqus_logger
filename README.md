# abaqus_logger

Simple table-style text logger for Abaqus and post-processing scripts.

```python
from abaqus_logger import SimpleLogger

logger = SimpleLogger(model_name="MyModel", work_dir="output")
logger.add_header("INITIALIZATION", pad=4)
logger.add("Init", "INFO", "Started")
logger.add_separator()
logger.save()  # writes <script_or_cae_name>_log.txt in work_dir
```

Install (editable): `pip install -e .`
