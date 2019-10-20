def lindenmayer(seed, rules, iters):
    for _ in range(iters):
        result = ""
        for axiom in seed:
            if axiom in rules:
                result += rules[axiom]
            else:
                result += axiom
        seed = result
    return seed


# ###DEMO###
# rule_dict = { "A": "ABA" , "B": "BC", "C": "BAC"}
# lind_list = [_ for _ in lindenmayer(seed='AB', rules=rule_dict, iters=5)]
# print(lind_list)
