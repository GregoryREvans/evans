import abjad
from evans.AttachmentHandlers.GlissandoHandler import GlissandoHandler
from evans.AttachmentHandlers.NoteheadHandler import NoteheadHandler
from evans.AttachmentHandlers.PitchHandler import PitchHandler
from evans.AttachmentHandlers.ArticulationHandler import ArticulationHandler
from evans.AttachmentHandlers.DynamicHandler import DynamicHandler
from evans.AttachmentHandlers.TextSpanHandler import TextSpanHandler
from evans.AttachmentHandlers.ClefHandler import ClefHandler
from evans.AttachmentHandlers.SlurHandler import SlurHandler
# from evans.AttachmentHandlers.GraceHandler import GraceHandler
from evans.AttachmentHandlers.TrillHandler import TrillHandler

class MusicMaker:
    def __init__(
        self,
        rmaker,
        glissando_handler=None,
        notehead_handler=None,
        pitch_handler=None,
        articulation_handler=None,
        dynamic_handler=None,
        text_span_handler=None,
        clef_handler=None,
        slur_handler=None,
        #grace_handler=None,
        trill_handler=None,
        continuous=False,
        state=None,
    ):
        self.glissando_handler = glissando_handler
        self.notehead_handler = notehead_handler
        self.pitch_handler = pitch_handler
        self.articulation_handler = articulation_handler
        self.dynamic_handler = dynamic_handler
        self.text_span_handler = text_span_handler
        self.clef_handler = clef_handler
        self.slur_handler = slur_handler
        #self.grace_handler = grace_handler
        self.trill_handler = trill_handler
        self.continuous = continuous
        self.rmaker = rmaker
        self.state = self.rmaker.state
        self._count = 0

    def __call__(self, durations):
        return self._make_music(durations)

    def _make_basic_rhythm(self, durations):
        if self.continuous == True:
            state = self.state
            selections = self.rmaker(durations, previous_state=self.rmaker.state)
            self.state = self.rmaker.state
        else:
            selections = self.rmaker(durations, )
        return selections

    def _make_music(self, durations):
        selections = self._make_basic_rhythm(durations)
        # if self.pitch_handler == None:
        #     start_command = abjad.LilyPondLiteral(
        #         r'\stopStaff \once \override Staff.StaffSymbol.line-count = #1 \startStaff',
        #         format_slot='before',
        #         )
        #     stop_command = abjad.LilyPondLiteral(
        #         r'\stopStaff \startStaff',
        #         format_slot='after',
        #         )
        #     literal = abjad.LilyPondLiteral(r'\once \override Staff.Clef.transparent = ##t', 'before')
        #     c_clef = abjad.LilyPondLiteral(r'\clef alto', 'before')
        #     abjad.attach(literal, selections[0][0])
        #     abjad.attach(c_clef, selections[0][0])
        #     abjad.attach(start_command, selections[0][0])
        #     abjad.attach(stop_command, selections[0][-1])
        # if self.grace_handler != None:
        #     selections = self.grace_handler(selections)
        if self.pitch_handler != None:
            selections = self.pitch_handler(selections)
            if self.clef_handler != None:
                selections = self.clef_handler(selections)
            if self.glissando_handler != None:
                selections = self.glissando_handler(selections)
            if self.trill_handler != None:
                selections = self.trill_handler(selections)
        if self.notehead_handler != None:
            selections = self.notehead_handler(selections)
        if self.articulation_handler != None:
            selections = self.articulation_handler(selections)
        if self.dynamic_handler != None:
            selections = self.dynamic_handler(selections)
        if self.text_span_handler != None:
            selections = self.text_span_handler(selections)
        if self.slur_handler != None:
            selections = self.slur_handler(selections)
        return selections
