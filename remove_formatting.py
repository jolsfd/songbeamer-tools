import os, sys
from typing import List


def filter(line: str, forbidden: List[str]) -> bool:
    for chars in forbidden:
        if line[1 : len(chars) + 1] == chars:
            return True

    return False


def end_of_editing(line, chars="---"):
    if line[: len(chars)] == chars:
        return True

    return False


def overwrite_format(
    filename: str,
    forbidden=[
        "Font",
        "FontSize",
        "BackgroundImage",
        "VerseOrder",
        "Chords",
        "Key",
        "Transpose",
        "Capo",
        "Speed",
        "Tempo",
        "Time",
    ],
    temporary_filename="temp.lock.txt",
) -> None:
    temp_path = os.path.join(os.path.dirname(filename), temporary_filename)

    with open(filename, "r", encoding="ISO-8859-1") as input:
        with open(temp_path, "w", encoding="ISO-8859-1") as output:
            editing = True

            for line in input:
                if editing:
                    line = line.replace(" ", "")

                    # check if editing is allowed
                    editing = not end_of_editing(line)

                    # nothing special found, write data to file
                    if not filter(line, forbidden):
                        output.write(line)

                    continue

                output.write(line)

    # Replace files
    os.replace(temp_path, filename)


def get_files(root: str, extensions=[".sng"]) -> List[str]:
    filenames = []

    for start_dir, dirs, files in os.walk(root, topdown=True):
        for filename in files:
            # print(filename)

            if os.path.splitext(filename)[1] in extensions:
                filenames.append(os.path.join(start_dir, filename))

    return filenames


def main(start_dir: str):
    print("Dateien einlesen...")
    files = get_files(start_dir)

    print("Formattierung löschen...")
    for filename in files:
        overwrite_format(filename)
        print(f"{os.path.basename(filename)}")

    print(f"Formattierung für {len(files)} erfolgreich entfernt.")


if __name__ == "__main__":
    print("=== Formattierung für .sng Dateien entfernen ===")

    print(f"Root: {sys.argv[1]}")

    main(sys.argv[1])
