# icon-gen

Generates a deterministic 128x128 PNG icon from any file. The icon is a color grid where each square's RGB value is derived from the SHAKE-256 hash of the input file — the same file always produces the same icon.

## Installation

```bash
uv sync
```

## Usage

```bash
uv run icon-gen <filepath> [options]
```

### Arguments

| Argument | Description |
|---|---|
| `filepath` | Path to the file to generate an icon for |

### Options

| Option | Default | Description |
|---|---|---|
| `-s`, `--squares` | `64` | Number of squares in the grid. Must be one of: `1`, `4`, `16`, `64` |
| `-n`, `--name` | `icon.png` | Output filename. Must end in `.png` |
| `-d`, `--dry-run` | off | Preview the image without saving it |

### Examples

```bash
# Generate icon for a file with default settings (64 squares, saved as icon.png)
uv run icon-gen myfile.bin

# 4x4 grid saved to a custom filename
uv run icon-gen myfile.bin --squares 16 --name myfile-icon.png

# Preview without saving
uv run icon-gen myfile.bin --dry-run
```

## How it works

1. The input file is hashed using SHAKE-256, producing 192 bytes of output
2. The 128x128 image is divided into a square grid of `--squares` cells
3. Each cell is filled with an RGB color taken from 3 consecutive bytes of the hash (1 byte per channel)
4. The grid reads left-to-right, top-to-bottom

With 64 squares and 3 bytes per square, all 192 hash bytes are consumed exactly once — every square gets a unique RGB value.

## Edge cases

- **`--squares` must be a power of 4** (`1`, `4`, `16`, `64`). Other values are rejected.
- **Output filename must end in `.png`**. Passing a non-`.png` name raises an error before any work is done.
- **`--dry-run` opens a system image viewer** and does not write any file. The output of `--name` is ignored in dry-run mode.
- **The input file must exist and be readable**. If it cannot be opened, the help text is printed and the process exits.
- **Icons are deterministic**: the same file always produces the same icon regardless of when or where the command is run.
