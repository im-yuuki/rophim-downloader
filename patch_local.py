from dotenv import load_dotenv
from os import getenv

load_dotenv()

prefix = getenv("MOVIE_ID")
if not prefix:
    print("MOVIE_ID is not set.")
    exit(1)

with open(f"out/{prefix}_variant.m3u8", "r", encoding="utf-8") as input_file:
    lines = input_file.readlines()

count = 1
for i, line in enumerate(lines):
    if line.startswith("http"):
        lines[i] = f"{prefix}_segment_{count}.ts\n"
        count += 1

with open(f"out/{prefix}.m3u8", "w", encoding="utf-8") as output_file:
    output_file.writelines(lines)


print(f"Patched playlist saved to out/{prefix}.m3u8")
print(f"Total segments patched: {count - 1}")
