import abjad

sieve_1a = abjad.index([0, 1, 7], 8)
sieve_1b = abjad.index([1, 3], 5)
sieve_1 = sieve_1a & sieve_1b
sieve_2a = abjad.index([0, 1, 2], 8)
sieve_2b = abjad.index([0], 5)
sieve_2 = sieve_2a & sieve_2b
sieve_3 = abjad.index([3], 8)
sieve_4 = abjad.index([4], 8)
sieve_5a = abjad.index([5, 6], 8)
sieve_5b = abjad.index([2, 3, 4], 5)
sieve_5 = sieve_5a & sieve_5b
sieve_6a = abjad.index([1], 8)
sieve_6b = abjad.index([2], 5)
sieve_6 = sieve_6a & sieve_6b
sieve_7a = abjad.index([6], 8)
sieve_7b = abjad.index([1], 5)
sieve_7 = sieve_7a & sieve_7b
sieve = sieve_1 | sieve_2 | sieve_3 | sieve_4 | sieve_5 | sieve_6 | sieve_7

# print(sieve.get_boolean_vector(total_length=40))
nums = [x for x in sieve.get_boolean_vector(total_length=100)]
list = [-12]
for x in nums:
    base = list[-1]
    list.append(base + 0.5)

sieve_list = []

for x, y in zip(nums, list):
    if x > 0:
        sieve_list.append(y)

# print(sieve_list)
notes = [abjad.Note(x, abjad.Duration(1, 8)) for x in sieve_list]
staff = abjad.Staff()
staff.extend(notes)
abjad.show(staff)
