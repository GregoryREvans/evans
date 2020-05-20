import abjad
from evans.AttachmentHandlers.CyclicList import CyclicList


class ArticulationHandler:
    def __init__(
        self,
        articulation_list=None,
        articulation_boolean_vector=[0],
        vector_continuous=True,
        continuous=False,
        count=-1,
        vector_count=-1,
        name="Articulation Handler",
    ):
        self.articulation_list = articulation_list
        self.vector_continuous = vector_continuous
        self.continuous = continuous
        self._count = count
        self._vector_count = vector_count
        self.articulation_boolean_vector = CyclicList(
            articulation_boolean_vector, self.vector_continuous, self._vector_count
        )
        self._cyc_articulations = CyclicList(
            lst=articulation_list, continuous=self.continuous, count=self._count
        )
        self.name = name

    def __call__(self, selections):
        self.add_articulations(selections)

    def add_articulations(self, selections):
        ties = abjad.select(selections).logical_ties(pitched=True)
        articulations = self._cyc_articulations(r=len(ties))
        vector = self.articulation_boolean_vector(r=len(ties))
        for tie, articulation, bool in zip(ties, articulations, vector):
            if bool == 0:
                if self.articulation_list is not None:
                    if articulation == "tremolo":
                        for leaf in tie:
                            if abjad.inspect(leaf).duration() <= abjad.Duration(1, 32):
                                continue
                            else:
                                abjad.attach(abjad.StemTremolo(32), leaf)
                    elif articulation == "default":
                        continue
                    else:
                        abjad.attach(abjad.Articulation(articulation), tie[0])
            else:
                continue

    def identifiers(self):
        return f"""articulation list:\n{self.articulation_list}\narticulation boolean vector\n{self.articulation_boolean_vector}\nvector continuous\n{self.vector_continuous}\ncontinuous\n{self.continuous},"""

    def name(self):
        return self.name

    def state(self):
        return f"""count\n{self._cyc_articulations.state()}\nvector count\n{self.articulation_boolean_vector.state()}"""


# ###DEMO###
# staff = abjad.Staff("c'4 c'4 c'4 r4 c'4 c'4 c'4 c'4 c'4")
# art_lst = ["staccato", "tenuto", "staccatissimo", "open", "halfopen", "stopped", "portato", "tremolo"]
# handler = ArticulationHandler(
#     articulation_list=art_lst,
#     articulation_boolean_vector=[0],
#     vector_continuous=True,
#     continuous=True,
# )
# handler(staff)
# abjad.show(staff)
