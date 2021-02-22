import abjad
import evans
from quicktions import Fraction

print("calculating basic ratios 1")

final_list = []

fundamental_pitch = abjad.NumberedPitch(-5)
fundamental_hertz = fundamental_pitch.hertz

ratios_1 = ["1/1", "2/1", "3/2", "5/3", "8/5", "13/8", "21/13"]
ratios_to_hertz_1 = [fundamental_hertz * Fraction(ratio) for ratio in ratios_1]
combination_ratios_1 = evans.herz_combination_tone_ratios(
    fundamental=fundamental_hertz,
    pitches=ratios_to_hertz_1,
    depth=1,
)
combination_ratios_1 = [
    "5/8",
    "1",
    "3/2",
    "13/8",
    "2",
    "5/2",
    "21/8",
    "3",
    "25/8",
    "7/2",
    "29/8",
]
combination_ratios_to_hertz_1 = [
    fundamental_hertz * Fraction(_) for _ in combination_ratios_1
]
print("calculating basic ratios 2")
ratios_2 = ["1/1", "2/1", "5/2", "12/5", "169/70", "408/169"]
ratios_to_hertz_2 = [fundamental_hertz * Fraction(ratio) for ratio in ratios_2]
combination_ratios_2 = [
    "1",
    "2",
    "5/2",
    "3",
    "7/2",
    "9/2",
]
combination_ratios_to_hertz_2 = [
    fundamental_hertz * Fraction(_) for _ in combination_ratios_2
]
print("calculating basic ratios 3")
combination_ratios_3 = [
    "5/8",
    "7/8",
    "9/8",
    "11/8",
    "13/8",
    "15/8",
    "17/8",
    "5/2",
    "11/4",
    "3",
    "13/4",
    "7/2",
    "15/4",
    "4",
    "17/4",
    "41/8",
    "11/2",
    "23/4",
    "13/2",
]
combination_ratios_to_hertz_3 = [
    fundamental_hertz * Fraction(_) for _ in combination_ratios_3
]
print("calculating basic ratios 4")
combination_ratios_4 = [
    "1",
    "3/2",
    "2",
    "5/2",
    "3",
    "7/2",
    "4",
    "9/2",
    "5",
    "11/2",
    "6",
    "13/2",
    "7",
    "15/2",
]
combination_ratios_to_hertz_4 = [
    fundamental_hertz * Fraction(_) for _ in combination_ratios_4
]

final_list.append(ratios_to_hertz_1)
final_list.append(ratios_to_hertz_2)
final_list.append(combination_ratios_to_hertz_1)
final_list.append(combination_ratios_to_hertz_3)
blend = list(set(combination_ratios_to_hertz_3 + combination_ratios_to_hertz_4))
final_list.append(blend)
final_list.append(combination_ratios_to_hertz_4)
final_list.append(combination_ratios_to_hertz_2)

print(final_list)
