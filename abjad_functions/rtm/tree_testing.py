import abjad
from evans.abjad_functions.rtm.rtm_maker import RTMMaker_4

maker = RTMMaker_4(rtm='(1 ((1 (1 1)) 1 (1 (1 1 1)) (1 (1 1)) 1))')
makers = [maker, ]
divisions = [abjad.Duration(4, 4), ]
staff = abjad.Staff()

def make_container(music_maker, durations):
    selections = music_maker(durations)
    container = abjad.Container([])
    container.extend(selections)
    return container

for music_maker, duration in zip(makers, divisions):
    durations = duration
    container = make_container(music_maker, durations)
    voice = staff
    voice.append(container)

score_file = abjad.LilyPondFile.new(
    voice,
    includes=['/Users/evansdsg2/evans/AttachmentHandlers/handler_tests/first_stylesheet.ily', '/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily'],
    )

###################

abjad.show(score_file)
