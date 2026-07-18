"""Inspect executable lookup paths."""

import os
import sys


EMPTY_ENTRY = "<empty>"


def split_path(path_value):
  """Return PATH entries without changing their order or contents."""
  return path_value.split(os.pathsep)


def find_duplicates(entries):
  """Return each entry's earlier position when it repeats a path."""
  first_positions = {}
  duplicates = {}

  for index, entry in enumerate(entries, start=1):
    normalized_entry = os.path.normcase(os.path.normpath(entry))
    if normalized_entry in first_positions:
      duplicates[index] = first_positions[normalized_entry]
    else:
      first_positions[normalized_entry] = index

  return duplicates


def render_entries(entries):
  """Format PATH entries as a numbered list."""
  index_width = len(str(len(entries)))
  duplicates = find_duplicates(entries)
  lines = []

  for index, entry in enumerate(entries, start=1):
    line = f"{index:>{index_width}}  {entry or EMPTY_ENTRY}"
    if index in duplicates:
      line += f"  (duplicate of entry {duplicates[index]})"
    lines.append(line)

  return lines


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
