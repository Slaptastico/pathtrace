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

  def test_finds_normalized_duplicate_entries(self):
    normalized_duplicate = os.path.join("first", ".")

    self.assertEqual(
      pathtrace.find_duplicates(["first", normalized_duplicate, "", ".", "second", "second"]),
      {2: 1, 4: 3, 6: 5},
    )

  def test_renders_numbered_entries(self):
    self.assertEqual(
      pathtrace.render_entries(["first", "", "third"]),
      ["1  first", "2  <empty>", "3  third"],
    )

  def test_renders_duplicate_entries(self):
    normalized_duplicate = os.path.join("first", ".")

    self.assertEqual(
      pathtrace.render_entries(["first", normalized_duplicate, "", "."]),
      [
        "1  first",
        f"2  {normalized_duplicate}  (duplicate of entry 1)",
        "3  <empty>",
        "4  .  (duplicate of entry 3)",
      ],
    )


class MainTest(unittest.TestCase):
  def test_prints_configured_path(self):
    normalized_duplicate = os.path.join("first", ".")
    path_value = os.pathsep.join(["first", normalized_duplicate])
    output = io.StringIO()

    with patch.dict(os.environ, {"PATH": path_value}, clear=True):
      with redirect_stdout(output):
        exit_code = pathtrace.main()

    self.assertEqual(exit_code, 0)
    self.assertEqual(
      output.getvalue(),
      f"1  first\n2  {normalized_duplicate}  (duplicate of entry 1)\n",
    )

  def test_reports_missing_path(self):
    output = io.StringIO()

    with patch.dict(os.environ, {}, clear=True):
      with redirect_stderr(output):
        exit_code = pathtrace.main()

    self.assertEqual(exit_code, 1)
    self.assertEqual(output.getvalue(), "pathtrace: PATH is not set\n")


if __name__ == "__main__":
  unittest.main()
