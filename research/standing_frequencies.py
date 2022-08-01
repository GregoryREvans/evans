def return_standing_frequencies(x, y, z, depth):
    out = []
    speed_of_sound = 1130
    starters = [x * 2, y * 2, z * 2]
    for distance in starters:
        fundamental_freq = speed_of_sound / distance
        partials = [_ + 1 for _ in range(depth)]
        sub_out = [fundamental_freq * _ for _ in partials]
        out.append(sub_out)
    return out


vals = return_standing_frequencies(8, 6, 6, depth=10)

for val in vals:
    print(val)
