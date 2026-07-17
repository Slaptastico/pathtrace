import io
import os
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

import pathtrace


class PathEntriesTest(unittest.TestCase):
  def test_preserves_order_and_empty_entries(self):
    path_value = os.pathsep.join(["first", "", "third"])

    self.assertEqual(pathtrace.split_path(path_value), ["first", "", "third"])

  def test_renders_numbered_entries(self):
    self.assertEqual(
      pathtrace.render_entries(["first", "", "third"]),
      ["1  first", "2  <empty>", "3  third"],
    )


class MainTest(unittest.TestCase):
  def test_prints_configured_path(self):
    path_value = os.pathsep.join(["first", "second"])
    output = io.StringIO()

    with patch.dict(os.environ, {"PATH": path_value}, clear=True):
      with redirect_stdout(output):
        exit_code = pathtrace.main()

    self.assertEqual(exit_code, 0)
    self.assertEqual(output.getvalue(), "1  first\n2  second\n")

  def test_reports_missing_path(self):
    output = io.StringIO()

    with patch.dict(os.environ, {}, clear=True):
      with redirect_stderr(output):
        exit_code = pathtrace.main()

    self.assertEqual(exit_code, 1)
    self.assertEqual(output.getvalue(), "pathtrace: PATH is not set\n")


if __name__ == "__main__":
  unittest.main()
