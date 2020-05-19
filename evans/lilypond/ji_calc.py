from math import log10

def ratio_to_cents(ratio):
    log_ratio = log10(ratio)
    log_2 = 1200 / log10(2)
    return log_ratio * log_2

print(
    ratio_to_cents(ratio=(16/15))
)

pythagorean_fifth = ratio_to_cents(ratio=(3/2))
syntonic_comma = ratio_to_cents(ratio=(81/80))
septimal_comma = ratio_to_cents(ratio=(64/63))
eleven_limit_undecimal_quarter_tone = ratio_to_cents(ratio=(33/32))
thirteen_limit_tridecimal_third_tone = ratio_to_cents(ratio=(27/26))
seventeen_limit_schisma = ratio_to_cents(ratio=(256/255))
nineteen_limit_schisma = ratio_to_cents(ratio=(513/512))
twenty_three_limit_comma = ratio_to_cents(ratio=(736/729))
