import os
import shutil
import tempfile
import unittest

from abaqus_logger import SimpleLogger


class SimpleLoggerTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_save_writes_aligned_table(self):
        logger = SimpleLogger("m", self.tmp, log_name="t")
        logger.add_header("INIT")
        logger.add("Init", "INFO", "short")
        logger.add("Load", "SUCCESS", "a longer message")
        logger.add_separator()
        logger.save()

        with open(os.path.join(self.tmp, "t_log.txt")) as f:
            lines = f.read().splitlines()

        self.assertIn("INIT", lines[0])
        self.assertEqual(len(lines[1]), len(lines[2]))
        self.assertEqual(set(lines[3]), {"-"})

    def test_save_creates_missing_work_dir(self):
        work_dir = os.path.join(self.tmp, "nested", "out")
        logger = SimpleLogger("m", work_dir, log_name="t")
        logger.add("Step", "INFO", "msg")
        logger.save()
        self.assertTrue(os.path.isfile(os.path.join(work_dir, "t_log.txt")))


if __name__ == "__main__":
    unittest.main()
