from fractions import Fraction


def is_prime(n):
    if n == 1:
        return False
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def prime_factors(n):
    prime_factor_list = []
    while not n % 2:
        prime_factor_list.append(2)
        n //= 2
    while not n % 3:
        prime_factor_list.append(3)
        n //= 3
    i = 5
    while n != 1:
        if is_prime(i):
            while not n % i:
                prime_factor_list.append(i)
                n //= i
        i += 2
    return prime_factor_list


def factorize_ratio(ratio):
    ratio = Fraction(ratio)
    numerator_factors = prime_factors(ratio.numerator)
    denominator_factors = prime_factors(ratio.denominator)
    return [numerator_factors, denominator_factors]


def ratio_to_pc(pitch, ratio):
    ratio = Fraction(ratio)
    vals = factorize_ratio(ratio)
    cumulative_accidentals = []
    for prime_list in vals:
        for prime in prime_list:
            continue
    return vals


print(ratio_to_pc("c", Fraction(3, 2)))
