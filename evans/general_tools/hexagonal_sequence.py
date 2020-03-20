def hexagonal_sequence(n_list=[1]):
    seq = []
    for n in n_list:
        x = n * (2 * n - 1)
        seq.append(x)
    return seq


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

# 
# seq = hexagonal_sequence(n_list=[_ for _ in range(8)])
# print(seq)
#
# mod_seq = mod(sequence=seq, modulus=7)
# print(mod_seq)
