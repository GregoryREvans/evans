\version "2.19.84"
\language "english"

#(set-default-paper-size "letterportrait")
#(set-global-staff-size 12)

\include "/Users/evansdsg2/evans/lilypond/evans-markups.ily"
\include "/Users/evansdsg2/evans/lilypond/evans-spanners.ily"
\include "/Users/evansdsg2/baca/lilypond/baca.ily"
\include "/Users/evansdsg2/abjad/docs/source/_stylesheets/ekmelos-ji-accidental-markups.ily"

\header {
	tagline = ##f

	breakbefore = ##t

	dedication = \markup
		\override #'(font-name . "STIXGeneral")
		\fontsize #3 {
			"Field Surveys (i)"
		}

	title = \markup
		\override #'(font-name . "STIXGeneral")
		\fontsize #12
		\center-column {
			"H u g a g"
			\vspace #1
		}

	subtitle = \markup
		\override #'(font-name . "STIXGeneral")
		\fontsize #-1
		\center-column {
			\line {
				"; or the Lesser Known and Fearsome Critters Inhabiting"
			}
			\line {
				"the Northeastern Forested Regions of North America"
			}
		}

	subsubtitle = \markup
		\override #'(font-name . "STIXGeneral")
		\fontsize #3
		\center-column {
			\with-color #white
			\line{
				"."
			}
			\fontsize #1
			\with-color #black
			\line{
				"f o r   s o l o   v i o l o n c e l l o"
			}
		}

	composer = \markup
		\override #'(font-name . "STIXGeneral")
		\center-column {
			\line{
				\fontsize #1 {
					"G r e g o r y  R o w l a n d  E v a n s (*1995)"
				}
			}
			\line{
				\vspace #4
			}
		}
}

dashedStaffSymbolLines =
#(define-music-function (parser location dash-space bool-list)
 ((number-pair? '(0.5 . 0.5)) list?)
#{
 \override Staff.StaffSymbol.after-line-breaking =
   #(lambda (grob)
     (let* ((staff-stencil (ly:grob-property grob 'stencil))
            (staff-line-positions
              (if (equal? (ly:grob-property grob 'line-positions) '() )
                '(-4 -2 0 2 4)
                (ly:grob-property grob 'line-positions)))
            (staff-width
              (interval-length
                (ly:stencil-extent staff-stencil X)))
            (staff-space (ly:staff-symbol-staff-space grob))
            (staff-line-thickness (ly:staff-symbol-line-thickness grob))
            (dash-width (car dash-space))
            (space-width (cdr dash-space))
            (sample-path `((moveto 0 0)
                           (lineto ,dash-width 0)
                           ))
            (dash-stencil
              (grob-interpret-markup
                grob
                (markup
                  #:path staff-line-thickness sample-path)))
           (dash-space-width (+ dash-width space-width))
            (count-dashes
              (inexact->exact
                (round
                  (/ staff-width
                     (- dash-space-width
                        staff-line-thickness)))))
            (dashed-stil
                (ly:stencil-aligned-to
                  (apply ly:stencil-add
                    (map
                      (lambda (x)
                        (ly:stencil-translate-axis
                          dash-stencil
                          (* (- dash-space-width staff-line-thickness) x)
                          X))
                      (iota count-dashes)))
                  Y
                  CENTER))
            (stil-x-length
              (interval-length
                (ly:stencil-extent dashed-stil  X)))
            (line-stil
              (make-line-stencil staff-line-thickness 0 0 staff-width 0))
            (corr-factor
              (/ staff-width (- stil-x-length staff-line-thickness)))
            (new-stil
              (apply
                ly:stencil-add
                  (map
                    (lambda (x y)
                      (ly:stencil-translate
                          (if (eq? y #f)
                            line-stil
                            (ly:stencil-scale
                              dashed-stil
                              corr-factor 1))
                          (cons (/ staff-line-thickness 2)
                                (* (/ x 2) staff-space))))
                    staff-line-positions bool-list))))

      (if (= (length bool-list)(length staff-line-positions))
        (ly:grob-set-property! grob 'stencil new-stil)
        (ly:warning
          "length of dashed line bool-list doesn't match the line-positions - ignoring"))))
#})

bowtab = {
   \override Clef.stencil = #ly:text-interface::print
   \override Clef.text = \markup { \general-align #Y #0.03
   \epsfile #Y #10 #"bow_position_tablature.eps"
   }
}

stringtab = {
   \override Clef.stencil = #ly:text-interface::print
   \override Clef.text = \markup { \general-align #X #-0.5 \general-align #Y #0.03
   \epsfile #Y #10 #"string_position_tablature.eps"
   }
}

\layout{
	\accidentalStyle dodecaphonic
    indent = #15
	ragged-last = ##t
    ragged-right = ##t
    \context {
        \name TimeSignatureContext
        \type Engraver_group
        \numericTimeSignature
        \consists Axis_group_engraver
		\consists Bar_number_engraver
        \consists Time_signature_engraver
		\consists Mark_engraver
		\consists Metronome_mark_engraver
		\consists Text_engraver
		\consists Text_spanner_engraver
		\override BarNumber.Y-extent = #'(0 . 0)
		\override BarNumber.Y-offset = 0
		\override BarNumber.extra-offset = #'(-4 . 0)
		\override BarNumber.font-name = "STIXGeneral"
		\override BarNumber.font-size = 3
		\override BarNumber.padding = 4
		\override MetronomeMark.X-extent = #'(0 . 0)
		\override MetronomeMark.Y-extent = #'(0 . 0)
		\override MetronomeMark.break-align-symbols = #'(left-edge)
		\override MetronomeMark.extra-offset = #'(0 . 1)
		\override MetronomeMark.stencil = ##f
		\override RehearsalMark.X-extent = #'(0 . 0)
		\override RehearsalMark.X-offset = 6
		\override RehearsalMark.Y-offset = -2.5
		\override RehearsalMark.break-align-symbols = #'(time-signature)
		\override RehearsalMark.break-visibility = #end-of-line-invisible
		\override RehearsalMark.font-name = "STIXGeneral"
		\override RehearsalMark.font-size = 3
		\override RehearsalMark.outside-staff-priority = 500
		\override RehearsalMark.self-alignment-X = #center
        \override TimeSignature.X-extent = #'(0 . 0)
        \override TimeSignature.X-offset = #ly:self-alignment-interface::x-aligned-on-self
        \override TimeSignature.Y-extent = #'(0 . 0)
        \override TimeSignature.break-align-symbol = ##f
        \override TimeSignature.break-visibility = #end-of-line-invisible
        \override TimeSignature.font-size = #4
		\override TimeSignature.font-name = "STIXGeneral"
        \override TimeSignature.self-alignment-X = #center
		\override TimeSignature.whiteout-style = #'outline
		\override TimeSignature.whiteout = ##t
        \override VerticalAxisGroup.default-staff-staff-spacing = #'((basic-distance . 9) (minimum-distance . 9) (padding . 4) (stretchability . 0))
    }
    \context {
        \Score
		\numericTimeSignature
		\remove Metronome_mark_engraver
        \remove Bar_number_engraver
		\remove Mark_engraver
        \accepts TimeSignatureContext
		\override BarLine.bar-extent = #'(0 . 0)
		\override BarLine.hair-thickness = #0.9
		\override BarLine.thick-thickness = #8
        \override Beam.breakable = ##t
		\override Beam.concaveness = #10000
		\override Clef.whiteout-style = #'outline
  		\override Clef.whiteout = 1
		\override DynamicText.font-size = #-2
		\override DynamicLineSpanner.staff-padding = 4
		\override DynamicLineSpanner.padding = 2
		\override Hairpin.bound-padding = #1
		\override Hairpin.padding = #2
		\override Glissando.breakable = ##t
		\override Glissando.thickness = #2
		\override Stem.thickness = #0.5
		\override Staff.thickness = #0.5
		\override MetronomeMark.font-size = 3
		\override NoteColumn.ignore-collision = ##t %
        \override SpacingSpanner.strict-grace-spacing = ##t
        \override StaffGrouper.staff-staff-spacing = #'((basic-distance . 14) (minimum-distance . 14) (padding . 2))
		\override Stem.stemlet-length = #1.15
		\override StemTremolo.beam-width = 1
		\override StemTremolo.beam-thickness = #0.3
        \override StemTremolo.flag-count = 4
        \override StemTremolo.slope = 0.5
		\override StemTremolo.slope = #0.3
		\override StemTremolo.shape = #'beam-like
		\override TupletBracket.bracket-visibility = ##t
        \override TupletBracket.minimum-length = #3
        \override TupletBracket.padding = #1.5
		\override TupletBracket.staff-padding = #1.3
        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
		\override TupletBracket.direction = #down % occasionally tweak up
		\override TupletNumber.font-size = #1
        \override TupletNumber.text = #tuplet-number::calc-fraction-text
		autoBeaming = ##f
		proportionalNotationDuration = #(ly:make-moment 2 24)
        tupletFullLength = ##t
    }
    \context {
        \StaffGroup
        %{ \name CelloGroup
        \type Engraver_group
        \alias StaffGroup %}
		\accepts StringContactStaff
		\accepts BeamStaff
        \accepts BowContactStaff
        \accepts BowAngleStaff
        \accepts DynamicStaff
		\accepts SubGroup
		\remove Metronome_mark_engraver
        \remove Bar_number_engraver
		\remove Mark_engraver
        systemStartDelimiter = #'SystemStartBracket
		\override VerticalAxisGroup.default-staff-staff-spacing = #'((basic-distance . 5) (minimum-distance . 5) (padding . 2))
		%{ \with {
			instrumentName = #"Violoncello"
			shortInstrumentName = #"vc."
		} %}
    }
	\context {
        \PianoStaff
        \name SubGroup
        \type Engraver_group
        \alias PianoStaff
        \accepts StringContactStaff
		\accepts BeamStaff
        \accepts BowContactStaff
        \accepts BowAngleStaff
        \accepts DynamicStaff
		\remove Metronome_mark_engraver
        \remove Bar_number_engraver
		\remove Mark_engraver
        %{ systemStartDelimiter = #'SystemStartSquare %}
		systemStartDelimiter = #'SystemStartBrace
		\override VerticalAxisGroup.default-staff-staff-spacing = #'((basic-distance . 1/2) (minimum-distance . 1/2) (padding . 0))
    }
    \context {
        \Staff
        \name StringContactStaff
        \type Engraver_group
        \alias Staff
        \remove Time_signature_engraver
		\remove Metronome_mark_engraver
        \remove Bar_number_engraver
		\remove Mark_engraver
		fontSize = #-1
        \override Glissando.bound-details.left.padding = #0.5
        \override Glissando.bound-details.right.padding = #0.5
        \override Glissando.thickness = #2
        \override Stem.direction = #down
        \override StaffSymbol.line-positions = #'(-8.2 -8 -6 -4 -2 -0.2 0 0.2 2 4 6 8 8.2)
		\dashedStaffSymbolLines #'(#t #t #t #t #t #t #f #f #f #f #f #f #f)
		\RemoveAllEmptyStaves
        \override VerticalAxisGroup.remove-first = ##t
        \hide BarLine
		%{ \stringtab %}
		\clef alto
		\override Clef.stencil = ##f
		\override Accidental.stencil = ##f
		\override AccidentalCautionary.stencil = ##f
		\with {
			instrumentName = #"SCP"
			shortInstrumentName = #"scp."
		}
    }
    \context {
        \Staff
        \name BowContactStaff
        \type Engraver_group
        \alias Staff
        \remove Time_signature_engraver
		\remove Metronome_mark_engraver
        \remove Bar_number_engraver
		\remove Mark_engraver
		fontSize = #-1
        \override Glissando.bound-details.left.padding = #0.5
        \override Glissando.bound-details.right.padding = #0.5
        \override Glissando.thickness = #2
        \override Stem.direction = #down
        \override StaffSymbol.line-positions = #'(-8.2 -8 8 8.2)
		\RemoveAllEmptyStaves
        \override VerticalAxisGroup.remove-first = ##t
        \hide BarLine
		\override NoteHead.no-ledgers = ##t
		%{ \bowtab %}
		\clef alto
		\override Clef.stencil = ##f

		\override Beam.stencil = ##f
		\override Dots.stencil = ##f
		\override Flag.stencil = ##f
		%{ \override NoteHead.Y-offset = #-5
		\override NoteHead.extra-offset = #'(0.05 . 0)
		\override NoteHead.stencil = ##f %}
		\override Rest.transparent = ##t
		\override Script.staff-padding = #2
		\override Stem.direction = #down
		\override Stem.stencil = ##f
		\override Tie.stencil = ##f
		\override TupletBracket.stencil = ##f
		\override TupletNumber.stencil = ##f
		\override Accidental.stencil = ##f
		\override AccidentalCautionary.stencil = ##f
    }
    \context {
        \Staff
        \name BowAngleStaff
        \type Engraver_group
        \alias Staff
        \remove Time_signature_engraver
		\remove Metronome_mark_engraver
        \remove Bar_number_engraver
		\remove Mark_engraver
		fontSize = #-1
        \override Glissando.bound-details.left.padding = #0.5
        \override Glissando.bound-details.right.padding = #0.5
        \override Glissando.thickness = #2
        \override Stem.direction = #down
        \override StaffSymbol.line-positions = #'(-15.2 -15 7 7.2)
		\RemoveAllEmptyStaves
        \override VerticalAxisGroup.remove-first = ##t
        \hide BarLine
		\override NoteHead.no-ledgers = ##t
		%{ \clef percussion %}
		\clef alto
		\override Clef.stencil = ##f

		\override Beam.stencil = ##f
		\override Dots.stencil = ##f
		\override Flag.stencil = ##f
		%{ \override NoteHead.Y-offset = #-5
		\override NoteHead.extra-offset = #'(0.05 . 0)
		\override NoteHead.stencil = ##f %}
		\override Rest.transparent = ##t
		\override Script.staff-padding = #2
		\override Stem.direction = #down
		\override Stem.stencil = ##f
		\override Tie.stencil = ##f
		\override TupletBracket.stencil = ##f
		\override TupletNumber.stencil = ##f
		\override Accidental.stencil = ##f
		\override AccidentalCautionary.stencil = ##f
    }
    \context {
        \Staff
        \remove Time_signature_engraver
		\remove Metronome_mark_engraver
        \remove Bar_number_engraver
		\remove Mark_engraver
		fontSize = #-1
        \hide BarLine
    }
    \context {
        \RhythmicStaff
        \name DynamicStaff
        \type Engraver_group
        \alias RhythmicStaff
        \remove Time_signature_engraver
		\remove Metronome_mark_engraver
        \remove Bar_number_engraver
		\remove Mark_engraver
		fontSize = #-1
        \override Stem.direction = #down
        \override StaffSymbol.line-positions = #'(0)
		\RemoveAllEmptyStaves
        \override VerticalAxisGroup.remove-first = ##t
        \hide BarLine
		%{ \clef percussion %}
		\with {
			instrumentName = #"Dynamics"
			shortInstrumentName = #"dyn."
		}
    }
    \context {
        \Voice
        \remove Forbid_line_break_engraver
    }
	\context {
		\Staff
        \name BeamStaff
        \type Engraver_group
        \alias Staff
        \remove Time_signature_engraver
		\remove Metronome_mark_engraver
        \remove Bar_number_engraver
		\remove Mark_engraver
		fontSize = #-1
		\clef "bass_15"
        \override StaffSymbol.line-positions = #'(0)
        \override VerticalAxisGroup.remove-first = ##t
        \hide BarLine

        \override Beam.direction = #down
        \override Beam.positions = #'(6 . 6)
        \override Clef.transparent = ##t
        \override Dots.staff-position = #2
		\override Rest.staff-position = #10
        \override Flag.Y-offset = #5
        \override NoteHead.no-ledgers = ##t
        \override NoteHead.transparent = ##t
        \override Script.staff-padding = #3
        \override Stem.direction = #down
        \override Stem.length = #7
        \override Stem.stem-begin-position = #19
        \override TimeSignature.stencil = ##f
		\override Tie.stencil = ##f
        \override TupletBracket.positions = #'(3 . 3)
		\RemoveAllEmptyStaves
		\override Accidental.stencil = ##f
		\override AccidentalCautionary.stencil = ##f
    }
}

\paper {
	system-separator-markup = \markup { \slashSeparator }
	system-system-spacing = #'((basic-distance . 13) (minimum-distance . 13) (padding . 4))

	indent = 20\mm
    short-indent = 15\mm
    bottom-margin = 8\mm
    left-margin = 8\mm
    right-margin = 8\mm
    top-margin = 8\mm

	oddHeaderMarkup = \markup ""
	evenHeaderMarkup = \markup ""
	oddFooterMarkup = \markup \fill-line {
	\override #'(font-name . "STIXGeneral")
	\bold \fontsize #2
    \concat {
      "Hugag -"
	  \fromproperty #'page:page-number-string "- GR Evans"
     }
  }
  evenFooterMarkup = \markup \fill-line {
	\override #'(font-name . "STIXGeneral")
	\bold \fontsize #2
	\concat { "Hugag -"
	\fromproperty #'page:page-number-string
	"- GR Evans"
    }
  }
}
