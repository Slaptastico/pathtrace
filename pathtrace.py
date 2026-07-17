"""Inspect executable lookup paths."""

import os
import sys


EMPTY_ENTRY = "<empty>"


def split_path(path_value):
  """Return PATH entries without changing their order or contents."""
  return path_value.split(os.pathsep)


def render_entries(entries):
  """Format PATH entries as a numbered list."""
  index_width = len(str(len(entries)))
  return [
    f"{index:>{index_width}}  {entry or EMPTY_ENTRY}"
    for index, entry in enumerate(entries, start=1)
  ]


def main():
  path_value = os.environ.get("PATH")
  if path_value is None:
    print("pathtrace: PATH is not set", file=sys.stderr)
    return 1

  for line in render_entries(split_path(path_value)):
    print(line)

  return 0


if __name__ == "__main__":
  raise SystemExit(main())
