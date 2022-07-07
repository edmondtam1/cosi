import re
from copy import deepcopy
import json

MAX_ROWS = 2
DEFAULT_TEMP = {"singers": "", "text": []}


def main():
    try:
        out = []
        with open("text.txt") as f:
            lines = f.readlines()

        temp = deepcopy(DEFAULT_TEMP)
        count = 0
        while count < len(lines):
            text = lines[count]
            if text == "\n":
                count += 1

            singers = lines[count].strip()
            temp["singers"] = singers
            try:
                while lines[count + 1] != "\n":
                    count += 1
                    if len(temp["text"]) >= MAX_ROWS:
                        out.append(temp)
                        temp = deepcopy(DEFAULT_TEMP) | {"singers": singers}

                    temp["text"].append(lines[count].strip())
            except IndexError as e:
                print("End of file reached")
                break

            count += 1
            out.append(temp)
            temp = deepcopy(DEFAULT_TEMP)

        out = [o | {"number": i} for i, o in enumerate(out)]
        text_json = json.dumps(out, indent=2)

        with open("text.json", "w") as f:
            f.write(text_json)

    except IOError:
        print("There was an error opening the file!")
        return

    with open("text.json") as f:
        text = json.load(f)
        for item in text:
            singers = item["singers"]
            text = item["text"]
            if singers == "Please turn your phone on silent mode":
                continue

            assert all(
                word
                in [
                    "All",
                    "Instrumental",
                    "Repeat",
                    "Guglielmo",
                    "Ferrando",
                    "Fiordiligi",
                    "Dorabella",
                    "Despina",
                    "Don",
                    "Alfonso",
                    "and",
                    "Act",
                    "1",
                    "2",
                    "End",
                ]
                for word in re.split(" |, ", singers)
                # for word in singers.split(" ")
            ), f"Wrong spelling for {item}"

        print("Tests passed!")


if __name__ == "__main__":
    main()
