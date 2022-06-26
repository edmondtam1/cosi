import json

MAX_ROWS = 2


def main():
    try:
        out = []
        with open("text.txt") as f:
            lines = f.readlines()

        temp = {"singers": "", "text": []}
        count = 0
        while count < len(lines):
            text = lines[count]
            if text.__contains__("Act "):
                count += 1
                temp["singers"] = text.strip()

            elif text == "\n":
                count += 1
                singers = lines[count].strip()
                temp["singers"] = singers

                try:
                    while lines[count + 1] != "\n":
                        count += 1
                        if len(temp["text"]) == MAX_ROWS:
                            out.append(temp)
                            temp = {"singers": singers, "text": []}

                        temp["text"].append(lines[count].strip())

                except IndexError as e:
                    print("End of file reached")
                count += 1

            out.append(temp)
            temp = {"singers": "", "text": []}

        text_json = json.dumps(out, indent=2)

        with open("text.json", "w") as f:
            f.write(text_json)

    except IOError:
        print("There was an error opening the file!")
        return


if __name__ == "__main__":
    main()
