# UPGRADE to n_dovan
def padovan(iters, seq=[1, 1, 1, 1]):
    final = []
    for n in range(iters):
        pPrevPrev, pPrev, pCurr, pNext = seq[0], seq[1], seq[2], seq[3]
        for i in range(3, n + 1):
            pNext = pPrevPrev + pPrev
            pPrevPrev = pPrev
            pPrev = pCurr
            pCurr = pNext
        final.append(pNext)
    return final


###DEMO###
# print(
#     padovan(
#         iters=20,
#         seq=[3, 5, 6, 4],
#         )
#     )
