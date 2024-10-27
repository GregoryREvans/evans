def text_to_morse(text):

    morse_dict = {
        "a": ".-",
        "b": "-...",
        "c": "-.-.",
        "d": "-..",
        "e": ".",
        "f": "..-.",
        "g": "--.",
        "h": "....",
        "i": "..",
        "j": ".---",
        "k": "-.-",
        "l": ".-..",
        "m": "--",
        "n": "-.",
        "o": "---",
        "p": ".--.",
        "q": "--.-",
        "r": ".-.",
        "s": "...",
        "t": "-",
        "u": "..-",
        "v": "...-",
        "w": ".--",
        "x": "-..-",
        "y": "-.--",
        "z": "--..",
        "á": ".--.-",
        "ä": ".-.-",
        "à": ".--.-",
        "é": "..-..",
        "è": ".-..-",
        "ñ": "--.--",
        "ö": "---.",
        "ó": "---.",
        "ü": "..---",
        " ": " ",  # Word separation
    }

    morse_code = ""
    for char in text.lower():
        if char in morse_dict:
            if char != " ":
                morse_code += morse_dict[char] + "˽"
            else:
                morse_code += morse_dict[char]
        else:
            continue

    return morse_code


def morse_to_durations(text):
    out = []
    cleaned_out = []
    for char in text:
        if char == ".":
            out.append(1)
        elif char == "-":
            out.append(3)
        elif char == "˽":
            out.append(-3)
        elif char == " ":
            out.append(-7)
        else:
            raise Exception(f"WRONG CHAR TYPE: {char}")
    for i, duration in enumerate(out):
        if i + 1 < len(out):
            if duration == -3 and out[i + 1] == -7:
                continue
            else:
                cleaned_out.append(duration)
    return cleaned_out


def morse_to_tuplets(text):
    out = []
    temp = []
    for char in text:
        if char == ".":
            temp.append(1)
        elif char == "-":
            temp.append(2)
        elif char == "˽":
            temp_tuple = tuple(temp)
            out.append(temp_tuple)
            temp = []
        elif char == " ":
            out.append((-1,))
        else:
            raise Exception(f"WRONG CHAR TYPE: {char}")
    return out


text = "La piedra es una frente donde los sueños gimen"
morse = text_to_morse(text)
print(morse)

print("")
rhythms = morse_to_durations(morse)
print(rhythms)

print("")
tuplets = morse_to_tuplets(morse)
print(tuplets)
