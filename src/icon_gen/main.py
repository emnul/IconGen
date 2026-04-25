import argparse
import hashlib
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

parser = argparse.ArgumentParser(
    prog="IconGen Anima v12589218731809213528796879521",
    description="Uses 100 billion Claude tokens to generate a 128x128 image",
)
parser.add_argument("filepath", type=Path)
parser.add_argument(
    "-s",
    "--squares",
    default=64,
    type=int,
    choices=[1, 4, 16, 64],
    help="Number of squares in the icon. Must be power of 4",
)
parser.add_argument(
    "-n", "--name", default="icon.png", type=str, help="Name of generated png file"
)
parser.add_argument(
    "-d",
    "--dry-run",
    action=argparse.BooleanOptionalAction,
    help="Do not save image file",
)

args = parser.parse_args()

IMAGE_SIZE = 128
HASH_SIZE = 192 * 2  # number of hex values needed to represent a 32 byte hash


def hash_file(filepath: Path):
    """Compute the hash of a file using the specified algorithm."""
    hash_func = hashlib.shake_256()
    try:
        with open(filepath, "rb") as file:
            # Read in chunks of 8192 bytes to handle large files
            for chunk in iter(lambda: file.read(8192), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest(192)
    except Exception as err:
        parser.print_help()
        sys.exit(f"\n{err}")


def hash_to_image(hash: str):
    if args.name[-4:] != ".png":
        raise ValueError("File extension must be .png")

    im = Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    side = math.isqrt(args.squares)
    row = col = side
    square_size = IMAGE_SIZE // side
    byte_index = 0

    for i in range(row):
        for j in range(col):
            top_left_corner = (j * square_size, i * square_size)
            bottom_right_corner = (
                (j * square_size) + square_size,
                (i + 1) * square_size,
            )
            stride = 6
            color_start = byte_index * stride
            r = int(hash[color_start : color_start + 2], 16)
            g = int(hash[color_start + 2 : color_start + 4], 16)
            b = int(hash[color_start + 4 : color_start + 6], 16)
            draw.rectangle([top_left_corner, bottom_right_corner], fill=(r, g, b))
            byte_index += 1

    if not args.dry_run:
        im.save(args.name)
    else:
        im.show()


def main():
    file_hash = hash_file(args.filepath)
    print(f"Hash of {args.filepath} is {file_hash[:6]}...{file_hash[-6:]}")
    hash_to_image(file_hash)


if __name__ == "__main__":
    main()
