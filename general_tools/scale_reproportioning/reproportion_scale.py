def reproportion_scale(base, partial_limit):
    step = base / 10.0
    end = partial_limit + 1
    scale = [_ for _ in range(2, end)]
    new_scale = [_ * step for _ in scale]
    print(new_scale)
    return new_scale

def reproportion_harmonics(fund, scale):
    calculated_series = [_ * fund for _ in scale]
    final_series = [fund,]
    final_series.extend(calculated_series)
    print(final_series)
    return final_series

###DEMO###
print(10)
insert_scale = reproportion_scale(base=10, partial_limit=17)
harmonics = reproportion_harmonics(20, insert_scale)
print(11)
insert_scale = reproportion_scale(base=11, partial_limit=17)
harmonics = reproportion_harmonics(20, insert_scale)
print(12)
insert_scale = reproportion_scale(base=12, partial_limit=17)
harmonics = reproportion_harmonics(20, insert_scale)
print(13)
insert_scale = reproportion_scale(base=13, partial_limit=17)
harmonics = reproportion_harmonics(20, insert_scale)
print(14)
insert_scale = reproportion_scale(base=14, partial_limit=17)
harmonics = reproportion_harmonics(20, insert_scale)
print(15)
insert_scale = reproportion_scale(base=15, partial_limit=17)
harmonics = reproportion_harmonics(20, insert_scale)
print(16)
insert_scale = reproportion_scale(base=16, partial_limit=17)
harmonics = reproportion_harmonics(20, insert_scale)
print(17)
insert_scale = reproportion_scale(base=17, partial_limit=17)
harmonics = reproportion_harmonics(20, insert_scale)
print(18)
insert_scale = reproportion_scale(base=18, partial_limit=17)
harmonics = reproportion_harmonics(20, insert_scale)
print(19)
insert_scale = reproportion_scale(base=19, partial_limit=17)
harmonics = reproportion_harmonics(20, insert_scale)
print(20)
insert_scale = reproportion_scale(base=20, partial_limit=17)
harmonics = reproportion_harmonics(20, insert_scale)
