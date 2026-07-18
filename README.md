# pathtrace

`pathtrace` is an early-stage command-line tool for explaining which executable appears first on `PATH` and why.

## Status

This project is in early development. There is no usable release yet.

## Try it

```console
python pathtrace.py
```

The current command prints each raw `PATH` entry in lookup order. Empty entries are shown as `<empty>`, later duplicate entries are marked with the earlier entry they repeat, and nonexistent entries are marked as `(not found)`.

## Planned scope

- List every matching executable in `PATH` order.
- Identify the first match.
- Flag duplicate and nonexistent `PATH` entries.
- Explain ordering and case differences that affect the result.
- Avoid executing discovered binaries unless explicitly requested.

## License

[MIT](LICENSE)
