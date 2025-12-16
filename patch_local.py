from dotenv import load_dotenv
from os import getenv
import pathlib

load_dotenv()

# prefix = getenv("MOVIE_ID")
# if not prefix:
#     print("MOVIE_ID is not set.")
#     exit(1)

def patch(prefix):
    path = pathlib.Path(f"out/{prefix}/{prefix}_variant.m3u8")
    if not path.exists():
        return

    with open(path, "r", encoding="utf-8") as input_file:
        lines = input_file.readlines()

    count = 1
    for i, line in enumerate(lines):
        if line.startswith("http"):
            lines[i] = f"{prefix}_segment_{count}.ts\n"
            count += 1

    path = pathlib.Path(f"out/{prefix}/{prefix}_variant.m3u8")
    with open(path, "w", encoding="utf-8") as output_file:
        output_file.writelines(lines)


    print(f"Patched playlist saved to out/{prefix}.m3u8")
    print(f"Total segments patched: {count - 1}")
