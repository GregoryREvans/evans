import abjad 
import tsmakers
from abjadext import rmakers 


timespan_maker = tsmakers.FloodedTimespanMaker()
abjad.f(timespan_maker)
music_specifiers = {
    'Violin Voice': 'violin music',
    'Cello Voice': 'cello music',
}
target_timespan = abjad.Timespan((1, 2), (2, 1))
timespan_list = timespan_maker(
    music_specifiers=music_specifiers,
    target_timespan=target_timespan,
)

abjad.f(timespan_list)


music_specifier = tsmakers.CompositeMusicSpecifier(
    primary_music_specifier='one',
    primary_voice_name='Viola 1 RH',
    rotation_indices=(0, 1, -1),
    secondary_voice_name='Viola 1 LH',
    secondary_music_specifier=tsmakers.MusicSpecifierSequence(
        application_rate='phrase',
        music_specifiers=['two', 'three', 'four'],
    ),
)
music_specifiers = {
    'Viola 1 Performer Group': music_specifier,
}
timespan_list = timespan_maker(
    music_specifiers=music_specifiers,
    target_timespan=target_timespan,
)


abjad.f(timespan_list)
abjad.show(timespan_list, scale=0.65)
