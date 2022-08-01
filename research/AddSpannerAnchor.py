import abjad

from ..handlers import DynamicHandler


class AddSpannerAnchor:
    def __init__(self, leaf, anchor_dur=None):
        self.leaf = leaf
        self.anchor_dur = anchor_dur

    def calc_anchor(self):
        durs = [self.leaf.written_duration, self.anchor_dur]
        container = abjad.Container()
        pre_mult = self.leaf.written_duration - self.anchor_dur
        mult = pre_mult / self.leaf.written_duration
        if isinstance(self.leaf, abjad.Chord):
            pitches = [abjad.NamedPitch(_) for _ in abjad.get.pitches(self.leaf)]
        elif isinstance(self.leaf, abjad.Note):
            pitches = [abjad.NamedPitch(_) for _ in abjad.get.pitches(self.leaf)]
            pitches = pitches[0]
        else:
            pass
        maker = abjad.LeafMaker()
        new_leaves = [list_ for list_ in maker([pitches], durs)]
        indicators = abjad.get.indicators(self.leaf)
        for indicator in indicators:
            abjad.attach(indicator, new_leaves[0][0])
        self.leaf.multiplier = mult
        abjad.attach(
            abjad.LilyPondLiteral(r"""\abjad-invisible-music""", format_slot="before"),
            new_leaves[1],
        )
        abjad.annotate(new_leaves[1], "type", "spanner anchor")
        container.extend(new_leaves)
        return container

    def add_anchor(self):
        abjad.mutate.replace(self.leaf, self.calc_anchor()[:])

    def add_spanner_anchor(self):
        if abjad.get.leaf(self.leaf, 1) is not None:
            next_leaf = abjad.get.leaf(self.leaf, 1)
            if abjad.get.annotation(next_leaf, "type") != "spanner anchor":
                self.add_anchor()
            else:
                pass
        else:
            self.add_anchor()


# #DEMO 1#
# staff = abjad.Staff("cs'4")
# anchor_maker1 = AddSpannerAnchor(leaf=staff[0], anchor_dur=abjad.Duration(1, 16))
# anchor_maker1.add_spanner_anchor()
# anchor_maker2 = AddSpannerAnchor(leaf=staff[0], anchor_dur=abjad.Duration(1, 16))
# anchor_maker2.add_spanner_anchor()
# print(abjad.lilypond(staff))
#
# #DEMO 2#
# staff = abjad.Staff("cs'4")
# a_leaf = abjad.Note("c'16")
# maker = AddSpannerAnchor(leaf=staff[0], anchor_leaf=a_leaf)
# maker.add_spanner_anchor()
# print(abjad.lilypond(staff))
#
# DEMO 3#
staff = abjad.Staff("c'4 c'4 c'4 r4 c'4 c'4 r8 c'8 c'4 r1")
selections = staff[:]
handler = DynamicHandler(
    dynamic_list=["f", "mp", "p", "mf", "ff"],
    flare_boolean_vector=[1, 0, 0, 1],
    flare_forget=False,
    forget=False,
    name="dynamic_handler_one",
)
for run in abjad.select.runs(selections):
    ties = abjad.select.logical_ties(run)
    maker = AddSpannerAnchor(leaf=ties[-1][-1], anchor_dur=abjad.Duration(1, 16))
    maker.add_spanner_anchor()
    new_ties = ties + [abjad.LogicalTie(items=maker.calc_anchor()[-1])]
    print("NEW TIES")
    print(new_ties)
    print("TIE 0")
    print(new_ties[0])
    print("TIE -1")
    print(new_ties[-1])
    handler(new_ties)
print(abjad.lilypond(staff))


# WHY DOES THE SPANNER ANCHOR ONLY EXIST AS A NOTE WITH NO LOGICAL TIE?
# WHY DOES ABJAD NOT RECOGNIZE THAT THE ANCHOR IS IN THE SELECTION?
# MULTIPLIERS DISAPPEAR AFTER abjad.show()
