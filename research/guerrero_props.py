def guerrero_props(p, t, s):
    return round((p * t) / s)

minutes = 20
phi = 1.6
section_size = 8
props = [1, ((section_size * 2) / phi), section_size, section_size, (((section_size * 2) / phi) / phi)]
prop_sum = sum(props)
total_duration = minutes * 60

for prop in props:
    section_duration = guerrero_props(prop, total_duration, prop_sum)
    print(f"Prop: {prop}\n SECONDS: {section_duration}\n MINUTES: {section_duration / 60}\n MM of 4/4 at 60: {section_duration / 4}\n\n")


# Prop: 1
#  SECONDS: 36
#  MINUTES: 0.6
#  MM of 4/4 at 60: 9.0
#
#
# Prop: 10.0
#  SECONDS: 361
#  MINUTES: 6.016666666666667
#  MM of 4/4 at 60: 90.25
#
#
# Prop: 8
#  SECONDS: 289
#  MINUTES: 4.816666666666666
#  MM of 4/4 at 60: 72.25
#
#
# Prop: 8
#  SECONDS: 289
#  MINUTES: 4.816666666666666
#  MM of 4/4 at 60: 72.25
#
#
# Prop: 6.25
#  SECONDS: 226
#  MINUTES: 3.7666666666666666
#  MM of 4/4 at 60: 56.5
