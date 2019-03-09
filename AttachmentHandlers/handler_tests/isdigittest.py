frac_string_list = ['1/2', '8/8', '3/4']
frac_numerators = []
frac_denominators = []
for frac in frac_string_list:
    if frac[0].isdigit() is True:
        frac_numerators.extend(frac[0])
    if frac[-1].isdigit() is True:
        frac_denominators.extend(frac[-1])
frac_tuples = [(num, denom) for num, denom in zip(frac_numerators, frac_denominators)]
result_list = []
for x in frac_tuples:
    y = x[0]
    z = x[-1]
    result_list.append(r'\markup {\center-align \vcenter \fraction ' + y + r' ' + z + r'}')
print(result_list)
