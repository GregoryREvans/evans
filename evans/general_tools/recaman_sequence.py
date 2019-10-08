def recaman_sequence(number):
    temp_list = []
    if number == 1:
        temp_list.append(number)
        return number
    else:
        a = recaman_sequence(number - 1)
        am = a - number
        ap = a + number
        if am > 0 and am not in temp_list:
            temp_list.append(am)
            return am
        else:
            temp_list.append(ap)
            return ap


def mod(sequence, modulus, indices=False):
    new_seq = [(_ % modulus) for _ in sequence]
    for i, _ in enumerate(new_seq):
        if indices is False:
            if _ == 0:
                new_seq[i] = _ + modulus
            else:
                continue
        else:
            continue
    return new_seq


seq = [recaman_sequence(number=_ + 1) for _ in range(80)]
print(seq)
mod_seq = mod(sequence=seq, modulus=7)
print(mod_seq)
