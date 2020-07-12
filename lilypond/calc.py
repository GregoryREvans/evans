acc = [
    "ff",
    "etf",
    "sef",
    "fxf",
    "tqf",
    "trf",
    "fef",
    "stf",
    "f",
    "ftf",
    "tef",
    "rf",
    "qf",
    "xf",
    "ef",
    "tf",
    "",
    "ts",
    "es",
    "xs",
    "qs",
    "rs",
    "tes",
    "fts",
    "s",
    "sts",
    "fes",
    "trs",
    "tqs",
    "fxs",
    "ses",
    "ets",
    "ss",
]

dia = ["c", "d", "e", "f", "g", "a", "b"]

all_notes = []

name_converter = {
    0: "Double-Flat",
    1: "Eleven-Twelf-Flat",
    2: "Seven-Eighth-Flat",
    3: "Five-Sixth-Flat",
    4: "Three-Quarter-Flat",
    5: "Two-Third-Flat",
    6: "Five-Eighth-Flat",
    7: "Seven-Twelf-Flat",
    8: "Flat",
    9: "Five-Twelf-Flat",
    10: "Three-Eighth-Flat",
    11: "Third-Flat",
    12: "Quarter-Flat",
    13: "Sixth-Flat",
    14: "Eighth-Flat",
    15: "Twelf-Flat",
    16: "Natural",
    17: "Twelf-Sharp",
    18: "Eighth-Sharp",
    19: "Sixth-Sharp",
    20: "Quarter-Sharp",
    21: "Third-Sharp",
    22: "Three-Eighth-Sharp",
    23: "Five-Twelf-Sharp",
    24: "Sharp",
    25: "Seven-Twelf-Sharp",
    26: "Five-Eighth-Sharp",
    27: "Two-Third-Sharp",
    28: "Three-Quarter-Sharp",
    29: "Five-Sixth-Sharp",
    30: "Seven-Eighth-Sharp",
    31: "Eleven-Twelf-Sharp",
    32: "Double-Sharp",
}

for i, x in enumerate(dia):
    for i_, y in enumerate(acc):
        all_notes.append(
            "(" + x + y + f" . ,(ly:make-pitch -1 {i} {name_converter[i_]}))"
        )

# print(all_notes)
