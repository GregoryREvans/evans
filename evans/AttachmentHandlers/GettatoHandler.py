import abjad
from evans.AttachmentHandlers.CyclicList import CyclicList


class GettatoHandler:
    r"""
    >>> staff = abjad.Voice("c'4 fs'4 c''4 gqs''4", name="Voice 1")
    >>> handler = evans.GettatoHandler(
    ...     number_of_attacks=[4, 5, 6],
    ...     actions=["throw", "drop"],
    ... )
    >>> handler(staff)
    >>> abjad.f(staff)
    \context Voice = "Voice 1"
    {
        <<
            \context Voice = "On_Beat_Grace_Container"
            {
                \set fontSize = #-4 %! abjad.on_beat_grace_container(1)
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                \once \override Beam.grow-direction = #left
                \slash %! abjad.on_beat_grace_container(2)
                \voiceOne %! abjad.on_beat_grace_container(3)
                <
                    \tweak font-size #0
                    \tweak transparent ##t
                    c'
                >32 * 4/3
                ^ \markup {
                    \hspace
                        #1
                    throw
                    (4)
                    }
                [
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                c'32 * 4/3
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                c'32 * 4/3
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                c'32 * 4/3
                ]
            }
            \context Voice = "Voice 1"
            {
                \voiceTwo %! abjad.on_beat_grace_container(4)
                c'4
            }
        >>
        <<
            \context Voice = "On_Beat_Grace_Container"
            {
                \set fontSize = #-4 %! abjad.on_beat_grace_container(1)
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                \once \override Beam.grow-direction = #right
                \slash %! abjad.on_beat_grace_container(2)
                \voiceOne %! abjad.on_beat_grace_container(3)
                <
                    \tweak font-size #0
                    \tweak transparent ##t
                    fs'
                >32 * 4/3
                ^ \markup {
                    \hspace
                        #1
                    drop
                    (5)
                    }
                [
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                fs'32 * 4/3
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                fs'32 * 4/3
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                fs'32 * 4/3
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                fs'32 * 4/3
                ]
            }
            \context Voice = "Voice 1"
            {
                \voiceTwo %! abjad.on_beat_grace_container(4)
                fs'4
            }
        >>
        <<
            \context Voice = "On_Beat_Grace_Container"
            {
                \set fontSize = #-4 %! abjad.on_beat_grace_container(1)
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                \once \override Beam.grow-direction = #left
                \slash %! abjad.on_beat_grace_container(2)
                \voiceOne %! abjad.on_beat_grace_container(3)
                <
                    \tweak font-size #0
                    \tweak transparent ##t
                    c''
                >32 * 4/3
                ^ \markup {
                    \hspace
                        #1
                    throw
                    (6)
                    }
                [
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                c''32 * 4/3
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                c''32 * 4/3
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                c''32 * 4/3
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                c''32 * 4/3
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                c''32 * 4/3
                ]
            }
            \context Voice = "Voice 1"
            {
                \voiceTwo %! abjad.on_beat_grace_container(4)
                c''4
            }
        >>
        <<
            \context Voice = "On_Beat_Grace_Container"
            {
                \set fontSize = #-4 %! abjad.on_beat_grace_container(1)
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                \once \override Beam.grow-direction = #right
                \slash %! abjad.on_beat_grace_container(2)
                \voiceOne %! abjad.on_beat_grace_container(3)
                <
                    \tweak font-size #0
                    \tweak transparent ##t
                    gqs''
                >32 * 4/3
                ^ \markup {
                    \hspace
                        #1
                    drop
                    (4)
                    }
                [
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                gqs''32 * 4/3
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                gqs''32 * 4/3
                \once \override NoteHead.no-ledgers = ##t
                \once \override Accidental.transparent = ##t
                \tweak transparent ##t
                gqs''32 * 4/3
                ]
            }
            \context Voice = "Voice 1"
            {
                \voiceTwo %! abjad.on_beat_grace_container(4)
                gqs''4
            }
        >>
    }

    """

    def __init__(
        self,
        number_of_attacks=[4, 5, 6],
        attack_number_continuous=True,
        actions=["throw", "drop"],
        action_continuous=True,
        boolean_vector=[1],
        vector_continuous=True,
        attack_count=-1,
        action_count=-1,
        vector_count=-1,
        name="Gettato Handler",
    ):
        self._attack_count = attack_count
        self._action_count = action_count
        self._vector_count = vector_count
        self.attack_number_continuous = attack_number_continuous
        self.action_continuous = action_continuous
        self.vector_continuous = vector_continuous
        self.attacks = CyclicList(
            number_of_attacks, self.attack_number_continuous, self._attack_count
        )
        self.actions = CyclicList(actions, self.action_continuous, self._action_count)
        self.boolean_vector = CyclicList(
            boolean_vector, self.vector_continuous, self._vector_count
        )
        self.name = name

    def __call__(self, selections):
        self.add_gettato(selections)

    def add_gettato(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        vector = self.boolean_vector(r=len(ties))
        for value, tie in zip(vector, ties):
            if value == 1:
                repetitions = self.attacks(r=1)[0]
                pitches = [_ for _ in abjad.inspect(tie[0]).pitches()]
                repeated_pitch = pitches[-1]
                list_ = []
                list_.append(abjad.Chord([repeated_pitch], (1, 32)))
                for _ in range(repetitions - 1):
                    list_.append(abjad.Note(repeated_pitch, (1, 32)))
                sel = abjad.Selection(list_)
                abjad.beam(sel)
                t = abjad.LilyPondLiteral(
                    [
                        r"\once \override NoteHead.no-ledgers = ##t",
                        r"\once \override Accidental.transparent = ##t",
                        r"\tweak transparent ##t",
                    ],
                    format_slot="before",
                )
                for leaf in abjad.select(sel).leaves():
                    abjad.attach(t, leaf)
                a = self.actions(r=1)[0]
                if a == "throw":
                    literal = abjad.LilyPondLiteral(
                        r"\once \override Beam.grow-direction = #left",
                        format_slot="before",
                    )
                    abjad.attach(literal, sel[0])
                    mark = abjad.Markup(
                        fr"\hspace #1 throw ({repetitions})", direction=abjad.Up
                    )
                    abjad.attach(mark, sel[0])
                elif a == "drop":
                    literal = abjad.LilyPondLiteral(
                        r"\once \override Beam.grow-direction = #right",
                        format_slot="before",
                    )
                    abjad.attach(literal, sel[0])
                    mark = abjad.Markup(
                        fr"\hspace#1 drop ({repetitions})", direction=abjad.Up
                    )
                    abjad.attach(mark, sel[0])
                else:
                    pass
                abjad.on_beat_grace_container(
                    sel,
                    tie[:],
                    leaf_duration=(1, 24),
                    do_not_slur=True,
                    do_not_beam=True,
                    font_size=-4,
                )

    def name(self):
        return self.name

    def state(self):
        return abjad.OrderedDict(
            [
                ("attack_count", self.attacks.state()),
                ("action_count", self.actions.state()),
                ("vector_count", self.boolean_vector.state()),
            ]
        )
