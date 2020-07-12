from ..CyclicList import CyclicList


def pitch_warp(
    warp_values=[0.5, -0.5], pitch_list=[0, 1, 2, 3, 4], boolean_vector=[0, 1, 1]
):
    warp_count = -1
    bool_count = -1
    w = CyclicList(warp_values, count=warp_count, continuous=True)
    b = CyclicList(boolean_vector, count=bool_count, continuous=True)
    bool_values = b(r=len(pitch_list))
    pairs = zip(bool_values, pitch_list)
    for i, pair in enumerate(pairs):
        if pair[0] == 1:
            if isinstance(pair[1], list):
                for p, _ in enumerate(pitch_list[i]):
                    warp_value = w(r=1)[0]
                    pitch_list[i][p] = pitch_list[i][p] + warp_value
            else:
                warp_value = w(r=1)[0]
                pitch_list[i] = pitch_list[i] + warp_value
    return pitch_list


# demo
# print(pitch_warp())
