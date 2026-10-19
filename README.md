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

## Install

From GitHub:

```
pip install git+https://github.com/guruprksh/abaqus_logger.git
```

From a local clone (editable):

```
pip install -e .
```

Inside Abaqus/CAE, copy `abaqus_logger.py` next to your script (or add its folder to `sys.path`).

## API

- `SimpleLogger(model_name, work_dir, log_name=None, overwrite=True)`
- `add(step, status, message)` - add a row (elapsed time is recorded automatically)
- `add_header(title, char="=", pad=2)` - centered section header
- `add_separator(char="-", length=None)` - horizontal line
- `save()` - write the aligned table to `<log_name>_log.txt` in `work_dir`

If `log_name` is not given, the Abaqus CAE file name is used, then the calling script name, then `unsaved_model`.
