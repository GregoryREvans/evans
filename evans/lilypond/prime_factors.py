from fractions import Fraction
from math import fmod, gcd, modf

print(3 % 2)
print(fmod(3, 2))
print(modf(Fraction(3, 2)))

circleoffifths = ["f", "c", "g", "d", "a", "e", "b"]


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


def power_of_prime_factor(integer, factor):
    factors = prime_factors(integer)
    return factors.count(factor)


def factorize_ratio(n, d):
    numerator_factors = prime_factors(n)
    denominator_factors = prime_factors(d)
    return [numerator_factors, denominator_factors]


def truncate(f, n):
    s = "{}".format(f)
    if "e" in s or "E" in s:
        return "{0:.{1}f}".format(f, n)
    i, p, d = s.partition(".")
    final = ".".join([i, (d + "0" * n)[:n]])
    return int(float(final))


def ratio_to_pc(ratio):
    # unfinished
    ratio = Fraction(ratio)
    primes = [
        Fraction(2),
        Fraction(3, 2),
        Fraction(5, 3),
        Fraction(7, 5),
        Fraction(11, 7),
        Fraction(13, 11),
        Fraction(17, 13),
        Fraction(19, 17),
        Fraction(23, 19),
    ]
    constituent_primes = []
    for prime in primes:
        if ratio == 1:
            remainder = "NO REMAINDER"
            pass
        else:
            constituent_primes.append([prime, truncate(float(ratio / prime), 0)])
            ratio = ratio / prime
            remainder = f"REMAINDER = {ratio}"
    return constituent_primes, remainder


print(ratio_to_pc(Fraction(17, 1)))

print(power_of_prime_factor(12, 2))
print(factorize_ratio(18, 16))
print(ratio_to_pc(12))

print(gcd(5, 3))
print(Fraction(5, 3))
