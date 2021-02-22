import itertools

import abjad
import evans

collection = "o*x."

out = []

for _ in range(5):
    val = _ + 1
    combs = [comb for comb in itertools.combinations_with_replacement(collection, val)]
    for comb in combs:
        perms = [perm for perm in itertools.permutations(comb)]
        for perm in perms:
            if perm[0] == "x" or perm[-1] == "x":
                continue
            elif 1 < len(perm) and perm[0] == ".":
                continue
            elif 1 < perm.count("."):
                continue
            else:
                out.append(perm)

out_set = {_ for _ in out}

final_list = []

for string_list in out_set:
    string = ""
    for char in string_list:
        string += char
    final_list.append(string)
    final_list.append(f"({string})")

final_list.sort()


combined_components = []

for _ in range(5):
    val = _ + 1
    combs = [
        comb for comb in itertools.combinations_with_replacement(collection, val)
    ]  # should be final_list
    for comb in combs:
        perms = [perm for perm in itertools.permutations(comb)]
        for perm in perms:
            total_length = 0
            for component in perm:
                if component[0] == "(":
                    component_ = component[1:-1]
                    component_length = len(component_)
                else:
                    component_length = len(component)
                total_length += component_length
            if 5 < total_length:
                continue
            else:
                combined_string = ""
                for component in perm:
                    combined_string += component
                combined_components.append(combined_string)

combined_components.sort()

final_combined_components = []

for _ in combined_components:
    if _[0] == "x" or _[-1] == "x":
        continue
    elif 1 < len(_) and _[0] == ".":
        continue
    elif _ == ".":
        continue
    elif _ == "x":
        continue
    elif 1 < _.count("."):
        continue
    else:
        final_combined_components.append(_)

final_combined_components = set(final_combined_components)

# for _ in final_combined_components:
#     print(_)
#     print("")


staff = abjad.Staff([abjad.Note("c'16") for _ in final_combined_components])
for string, note in zip(final_combined_components, staff):
    markup = evans.Damping(string, direction=abjad.Up).markup()
    abjad.attach(markup, note)

abjad.show(staff)
