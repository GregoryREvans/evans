import abjad


class AddSpannerAnchor:
    def __init__(
        self,
        leaf,
        anchor_dur=None,
        anchor_leaf=None,
    ):
        self.leaf = leaf
        self.anchor_dur = anchor_dur
        self.anchor_leaf = anchor_leaf

    def calc_anchor(self):
        if self.anchor_leaf is not None:
            self.anchor_dur = self.anchor_leaf.written_duration
            durs = [self.leaf.written_duration]
        else:
            durs = [self.leaf.written_duration, self.anchor_dur]
        container = abjad.Container()
        pre_mult = self.leaf.written_duration - self.anchor_dur
        mult = pre_mult / self.leaf.written_duration
        if isinstance(self.leaf, abjad.Chord):
            pitches = [abjad.NamedPitch(_) for _ in abjad.inspect(self.leaf).pitches()]
        elif isinstance(self.leaf, abjad.Note):
            pitches = [abjad.NamedPitch(_) for _ in abjad.inspect(self.leaf).pitches()]
            pitches = pitches[0]
        else:
            pass
        maker = abjad.LeafMaker()
        new_leaves = [l for l in maker([pitches], durs)]
        new_leaf = new_leaves[0]
        indicators = abjad.inspect(self.leaf).indicators()
        for indicator in indicators:
            abjad.attach(indicator, new_leaf)
        new_leaf.multiplier = mult
        self.leaf.multiplier = mult
        if self.anchor_leaf is not None:
            anchor = self.anchor_leaf
            l = [_ for _ in abjad.inspect(self.leaf).pitches()]
            anchor.written_pitch = l[0]
        else:
            anchor = new_leaves[1]
        abjad.attach(abjad.LilyPondLiteral(r"""\abjad-invisible-music""", format_slot="before"), anchor)
        abjad.annotate(anchor, "type", "spanner anchor")
        container.append(new_leaf)
        container.append(anchor)
        return container

    def add_anchor(self):
        abjad.mutate(self.leaf).replace(self.calc_anchor()[:])

    def add_spanner_anchor(self):
        if abjad.inspect(self.leaf).leaf(1) is not None:
            next_leaf = abjad.inspect(self.leaf).leaf(1)
            if abjad.inspect(next_leaf).annotation("type") != "spanner anchor":
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
# abjad.f(staff)
#
# #DEMO 2#
# staff = abjad.Staff("cs'4")
# a_leaf = abjad.Note("c'16")
# maker = AddSpannerAnchor(leaf=staff[0], anchor_leaf=a_leaf)
# maker.add_spanner_anchor()
# abjad.f(staff)
#
#DEMO 3#
staff = abjad.Staff("c'4 c'4 c'4 r4 c'4 c'4 r8 c'8 c'4 r1")
selections = abjad.select(staff[:])
new_selections = abjad.Selection()
for run in abjad.select(selections).runs():
    ties = abjad.select(run).logical_ties()
    maker = AddSpannerAnchor(leaf=ties[-1][-1], anchor_dur=abjad.Duration(1, 16))
    maker.add_spanner_anchor()
    sel = abjad.select(run)
    tail = abjad.select(maker.calc_anchor()[-1])
    print(sel)
    new_selections + sel
    print(new_selections)
    new_selections + tail
    print(new_selections)

#DOESN'T WORK
#Maybe allow attachments by hand
#in dynamic and text span handler, go through process of attachments while compiling a list of things to attach to anchor, then attach them all?
