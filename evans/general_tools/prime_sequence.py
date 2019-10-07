def prime_sequence(start, end):
    seq = []
    for val in range(start, end + 1):
        if val > 1:
            for n in range(2, val):
                if (val % n) == 0:
                    break
                else:
                    if val not in seq:
                        seq.append(val)
                    else:
                        continue
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

primes = prime_sequence(start=11, end=25)
print(primes)
mod_seq = mod(sequence=primes, modulus=7)
print(mod_seq)
