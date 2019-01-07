import abjad
import abjadext.rmakers


"""There are a *small* handful of issues with this code.





You also confuse when to use your variable "pitch" vs "pitches"""


rhythm_maker = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(
        counts=[1, 2, -1, 1, 4, 1, 1],
        denominator=16,
        ),
    )

divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
selections = rhythm_maker(divisions)

all_pitches = [0, 11, [5, 15], 6, 7, 1, -5, 26, 0] * 2

logical_ties = abjad.iterate(selections).logical_ties(pitched=True)

'''
    PART 1: Commentary on Old file

    In the following loop, your variables are all mismatched,
    so it becomes difficult to know which variables are being passed to what location.
    Try to keep everything in the same order like so:

        for item-x, item-y in zip(list-x, list-y):

    You see? In yours, you switch the order,
    so you are referring to logical_tie objects by the name "pitch" which is very confusing.
    So now you say:

    for old_leaf in logical_tie:

    *This is now asking your pitch for objects within itself because you misnamed your variables*
    So if we change the variable names to the correct names, we still get the same traceback error as before!
    Why is this?
    Is this problem is not simply fixed by switching the variable names to more useable identifiers?
    The *new* problem lies in your query for length. You are looking at each item in your list and sking its length.
    What is in that list? Integers and other lists.
    A list has a length, but an integer does not. An integer is inherently a single object,
    so it does not posses a length attribute, because this would typically be redundant.

    What you *really* want to be querying is whether or not the object is an integer or a list.
    This would be done with:

        isinstance()

    Even if we get the use of isinstance correct, there are still a number of problems we will run into!
    You are trying to replace the old_leaf with a new_leaf. This requires that the leaf has *parentage*.
    Simply put, parentage is all of the information that desribes where an item sits within our score such as:
        Which score is it in?
        Which staff is it in?
        Which measure is it in?
        What items precede it?
        What items follow it?
        etc...
    But
        selections = rhythm_maker(divisions)
    Is not sitting in a score or a staff or a voice or a measure, in fact it is just a list.
    It is a special list called a selection, but it is still a list.
    All of that parentage information is not quite real yet.
    We need to put those notes in a staff or a container or something before we can replace things.
    You can't mutate selections.

    Now for our final issue.
    We need to clean up our score creation.
    You want the floating time signatures, and
        abjad.LilyPondFile.rhythm()
    is a nice little shortcut to get them, but this will not be a good solution in the long run.
    What we really need is to define a
        Global Context
    in Lilypond that contains *very little* other than our time signatures.
    I typically define these myself in my own stylesheets, but there is a default abjad one in the abjad stylesheets.

    A staff is a kind of context.
    Our global context will basically be a staff with all of the unnecessary things removed.
    We need to fill this staff with
        abjad.Skip()
    objects of the same number of measures we have.
    We also want to make sure these skips are the same length as the time signatures we created.
    We need to attach our time signatures to these skips and add both this context and our music into our score.

    You can do this the way you have been in the past,
    but perhaps we can speed things up by defining our score structure and then filling that structure with information.
    If we name all of our staff objects and global contexts, we can refer to them by name, like a variable.

    Continue to PART 2 in new file.
'''

for pitches, logical_tie in zip(logical_ties, all_pitches):
    for old_leaf in logical_tie:
        if len(pitches) == 1:
            old_leaf.written_pitch = pitches[0]
        elif len(pitches) > 1:
            new_leaf = abjad.Chord(pitches, old_leaf.written_duration)
            abjad.mutate(old_leaf).replace(new_leaf)

lilypond_file = abjad.LilyPondFile.rhythm(
    selections,
    divisions,
    )

abjad.show(lilypond_file)
