import abjad

def hz_to_hz_from_ratio(hz=440, ratio=(7/4)):
    return hz * ratio


just_pitch = hz_to_hz_from_ratio(
        hz=261.625565,
        ratio=736/729
)

note = abjad.NamedPitch().from_hertz(
    just_pitch
)

abjad_pitch = note.hertz

# print(just_pitch - abjad_pitch)
# print(just_pitch)
# print(abjad_pitch)
# print(just_pitch - 261.625565)

syntonic_comma_hertz = 3.270319562499992
septimal_comma_hertz = 4.1527867460317225
eleven_limit_undecimal_quarter_tone_hertz = 0.5095843792258847
thirteen_limit_tridecimal_third_tone_hertz = 8.175798906250009
seventeen_limit_schisma_hertz = 1.0259826078431615
nineteen_limit_schisma_hertz = 0.5109874316406149
twenty_three_limit_comma_hertz = 2.5121796364883267
