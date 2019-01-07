import abjad
import abjadext.rmakers

'''
    Here we have defined our entire score stucture.
    We have named everything too! We can refer to things by using a syntax like this:
        score['name']
    We could call for Staff 1 or Voice 1 or Global Context,
    but its important to remember that you are referring to the name and *not* the lilypond_type.
'''

score = abjad.Score([
    abjad.Staff(lilypond_type='GlobalContext', name='Global Context'),
    abjad.StaffGroup(
        [
            abjad.Staff([abjad.Voice(name='Voice 1')],name='Staff 1', lilypond_type='Staff',),
        ],
        name='Staff Group',
    ),
],
)

'''
    We can create the rmakers like normal.
'''

rhythm_maker = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(
        counts=[1, 2, -1, 1, 4, 1, 1],
        denominator=16,
        ),
    )

'''
    We need a slightly fancier structure for time signature creation.
        LilyPondFile.rhythm()
    did some of this for us in the past, but here we do it ourselves.
    This is what is called a list comprehension.
    It is a very common way of building lists out of things in python.

    Here we are creating a new list out of an old one.
    Our old list was
        [(3, 8), (4, 8), (3, 8), (4, 8)]
    but our new list is
        [abjad.TimeSignature(3, 8), abjad.TimeSignature(4, 8), abjad.TimeSignature(3, 8), abjad.TimeSignature(4, 8), ]
'''

time_signatures = [
    abjad.TimeSignature(pair) for pair in [
        (3, 8), (4, 8), (3, 8), (4, 8)
        ]
]

'''
    Now we create the skips like I described in the last file.
    We change the length of the skips based on the lengths of the time signatures,
    then we append them to our Global Context with the sytax we saw at the top of this file.
'''

for time_signature in time_signatures:
    skip = abjad.Skip(1, multiplier=(time_signature))
    abjad.attach(time_signature, skip)
    score['Global Context'].append(skip)

'''
    We can still make our rhythm and pitch lists like normal.
'''

rhythms = rhythm_maker(time_signatures)
pitch_list = [0, 11, [5, 15], 6, 7, 1, -5, 26, 0] * 2

'''
    Here you can see a cleaned up version of what you alerady had going.
    All of the variables are organized appropriately and there is no longer any confusion between the variables
        pitch
    and
        pitches

    You will also notice that we are no longer querying integers for their length,
    instead we are asking if each item in our list is an instance of an
        int
    or
        list
    which are how we refer to the python data types of integers and lists
'''

for voice in abjad.select(score['Staff 1']).components(abjad.Voice):
    voice.extend(rhythms)
    logical_ties = abjad.iterate(voice).logical_ties(pitched=True)
    for pitch, logical_tie in zip(pitch_list, logical_ties):
        for old_leaf in logical_tie:
            if isinstance(pitch, int):
                old_leaf.written_pitch = pitch
            elif isinstance(pitch, list):
                new_leaf = abjad.Chord(pitch, old_leaf.written_duration)
                abjad.mutate(old_leaf).replace(new_leaf)

'''
    Now here is where all of this work pays off.
    Instead of LilyPondFile.rhythm, we use

        abjad.LilyPondFile.new()

    This allows us to insert more than "selections" and "divisions" which can get quite restrictive.
    Now we can put in our entire score.

    But most importantly,
    we can now add include statements to our lilypond file.
    I have included files from my own abjad directory,
    you will have to change the file path to match where these files are on your own computer,
    but they are included in abjad.

    These files handle some basic formatting things,
    but specifically the
        rhythm-maker-docs.ily
    contains a definitions of a *basic* global context which gives us our floating time signatures.
'''

file = abjad.LilyPondFile.new(
    score,
    includes=[
        '/Users/evansdsg2/abjad/docs/source/_stylesheets/default.ily',
        '/Users/evansdsg2/abjad/docs/source/_stylesheets/rhythm-maker-docs.ily',
            ],
    )

'''
    Finally we show our file that we made.
    Just like LilyPondFile.rhythm,
        abjad.show()
    is a shortcut for various forms of
        abjad.persist()

    I can show you some fancy things with persist later if you want, but for now this should be a good step forward.

    Happy composing.
'''

abjad.show(file)
