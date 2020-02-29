\version "2.19.84"
\language "english"
\include "evans-accidentals.ily"

#(define-public Double-Sharp  8/8)
#(define-public Eleven-Twelf-Sharp 11/12)
#(define-public Seven-Eighth-Sharp  7/8)
#(define-public Five-Sixth-Sharp 5/6)
#(define-public Three-Quarter-Sharp  3/4)
#(define-public Two-Third-Sharp 2/3)
#(define-public Five-Eighth-Sharp  5/8)
#(define-public STwelf-Sharp 7/12)
#(define-public Sharp  1/2)
#(define-public Five-Twelf-Sharp 5/12)
#(define-public Three-Eighth-Sharp  3/8)
#(define-public Third-Sharp 1/3)
#(define-public Quarter-Sharp  1/4)
#(define-public Sixth-Sharp 1/6)
#(define-public Eighth-Sharp  1/8)
#(define-public Twelf-Sharp 1/12)
#(define-public Natural 0/1)
#(define-public Twelf-Flat  -1/12)
#(define-public Eighth-Flat  -1/8)
#(define-public Sixth-Flat  -1/6)
#(define-public Quarter-Flat  -1/4)
#(define-public Third-Flat  -1/3)
#(define-public Three-Eighth-Flat  -3/8)
#(define-public Five-Twelf-Flat  -5/12)
#(define-public Flat  -1/2)
#(define-public STwelf-Flat  -7/12)
#(define-public Five-Eighth-Flat  -5/8)
#(define-public Two-Third-Flat  -2/3)
#(define-public Three-Quarter-Flat  -3/4)
#(define-public Five-Sixth-Flat  -5/6)
#(define-public Seven-Eighth-Flat  -7/8)
#(define-public Eleven-Twelf-Flat  -11/12)
#(define-public Double-Flat  -8/8)

newPitchNames = #`(
    (cff . ,(ly:make-pitch -1 0 Double-Flat))
    (cetf . ,(ly:make-pitch -1 0 Eleven-Twelf-Flat))
    (csef . ,(ly:make-pitch -1 0 Seven-Eighth-Flat))
    (cfxf . ,(ly:make-pitch -1 0 Five-Sixth-Flat))
    (ctqf . ,(ly:make-pitch -1 0 Three-Quarter-Flat))
    (ctrf . ,(ly:make-pitch -1 0 Two-Third-Flat))
    (cfef . ,(ly:make-pitch -1 0 Five-Eighth-Flat))
    (cstf . ,(ly:make-pitch -1 0 STwelf-Flat))
    (cf . ,(ly:make-pitch -1 0 Flat))
    (cftf . ,(ly:make-pitch -1 0 Five-Twelf-Flat))
    (ctef . ,(ly:make-pitch -1 0 Three-Eighth-Flat))
    (crf . ,(ly:make-pitch -1 0 Third-Flat))
    (cqf . ,(ly:make-pitch -1 0 Quarter-Flat))
    (cxf . ,(ly:make-pitch -1 0 Sixth-Flat))
    (cef . ,(ly:make-pitch -1 0 Eighth-Flat))
    (ctf . ,(ly:make-pitch -1 0 Twelf-Flat))
    (c . ,(ly:make-pitch -1 0 Natural))
    (cts . ,(ly:make-pitch -1 0 Twelf-Sharp))
    (ces . ,(ly:make-pitch -1 0 Eighth-Sharp))
    (cxs . ,(ly:make-pitch -1 0 Sixth-Sharp))
    (cqs . ,(ly:make-pitch -1 0 Quarter-Sharp))
    (crs . ,(ly:make-pitch -1 0 Third-Sharp))
    (ctes . ,(ly:make-pitch -1 0 Three-Eighth-Sharp))
    (cfts . ,(ly:make-pitch -1 0 Five-Twelf-Sharp))
    (cs . ,(ly:make-pitch -1 0 Sharp))
    (csts . ,(ly:make-pitch -1 0 STwelf-Sharp))
    (cfes . ,(ly:make-pitch -1 0 Five-Eighth-Sharp))
    (ctrs . ,(ly:make-pitch -1 0 Two-Third-Sharp))
    (ctqs . ,(ly:make-pitch -1 0 Three-Quarter-Sharp))
    (cfxs . ,(ly:make-pitch -1 0 Five-Sixth-Sharp))
    (cses . ,(ly:make-pitch -1 0 Seven-Eighth-Sharp))
    (cets . ,(ly:make-pitch -1 0 Eleven-Twelf-Sharp))
    (css . ,(ly:make-pitch -1 0 Double-Sharp))

    (dff . ,(ly:make-pitch -1 1 Double-Flat))
    (detf . ,(ly:make-pitch -1 1 Eleven-Twelf-Flat))
    (dsef . ,(ly:make-pitch -1 1 Seven-Eighth-Flat))
    (dfxf . ,(ly:make-pitch -1 1 Five-Sixth-Flat))
    (dtqf . ,(ly:make-pitch -1 1 Three-Quarter-Flat))
    (dtrf . ,(ly:make-pitch -1 1 Two-Third-Flat))
    (dfef . ,(ly:make-pitch -1 1 Five-Eighth-Flat))
    (dstf . ,(ly:make-pitch -1 1 STwelf-Flat))
    (df . ,(ly:make-pitch -1 1 Flat))
    (dftf . ,(ly:make-pitch -1 1 Five-Twelf-Flat))
    (dtef . ,(ly:make-pitch -1 1 Three-Eighth-Flat))
    (drf . ,(ly:make-pitch -1 1 Third-Flat))
    (dqf . ,(ly:make-pitch -1 1 Quarter-Flat))
    (dxf . ,(ly:make-pitch -1 1 Sixth-Flat))
    (def . ,(ly:make-pitch -1 1 Eighth-Flat))
    (dtf . ,(ly:make-pitch -1 1 Twelf-Flat))
    (d . ,(ly:make-pitch -1 1 Natural))
    (dts . ,(ly:make-pitch -1 1 Twelf-Sharp))
    (des . ,(ly:make-pitch -1 1 Eighth-Sharp))
    (dxs . ,(ly:make-pitch -1 1 Sixth-Sharp))
    (dqs . ,(ly:make-pitch -1 1 Quarter-Sharp))
    (drs . ,(ly:make-pitch -1 1 Third-Sharp))
    (dtes . ,(ly:make-pitch -1 1 Three-Eighth-Sharp))
    (dfts . ,(ly:make-pitch -1 1 Five-Twelf-Sharp))
    (ds . ,(ly:make-pitch -1 1 Sharp))
    (dsts . ,(ly:make-pitch -1 1 STwelf-Sharp))
    (dfes . ,(ly:make-pitch -1 1 Five-Eighth-Sharp))
    (dtrs . ,(ly:make-pitch -1 1 Two-Third-Sharp))
    (dtqs . ,(ly:make-pitch -1 1 Three-Quarter-Sharp))
    (dfxs . ,(ly:make-pitch -1 1 Five-Sixth-Sharp))
    (dses . ,(ly:make-pitch -1 1 Seven-Eighth-Sharp))
    (dets . ,(ly:make-pitch -1 1 Eleven-Twelf-Sharp))
    (dss . ,(ly:make-pitch -1 1 Double-Sharp))

    (eff . ,(ly:make-pitch -1 2 Double-Flat))
    (eetf . ,(ly:make-pitch -1 2 Eleven-Twelf-Flat))
    (esef . ,(ly:make-pitch -1 2 Seven-Eighth-Flat))
    (efxf . ,(ly:make-pitch -1 2 Five-Sixth-Flat))
    (etqf . ,(ly:make-pitch -1 2 Three-Quarter-Flat))
    (etrf . ,(ly:make-pitch -1 2 Two-Third-Flat))
    (efef . ,(ly:make-pitch -1 2 Five-Eighth-Flat))
    (estf . ,(ly:make-pitch -1 2 STwelf-Flat))
    (ef . ,(ly:make-pitch -1 2 Flat))
    (eftf . ,(ly:make-pitch -1 2 Five-Twelf-Flat))
    (etef . ,(ly:make-pitch -1 2 Three-Eighth-Flat))
    (erf . ,(ly:make-pitch -1 2 Third-Flat))
    (eqf . ,(ly:make-pitch -1 2 Quarter-Flat))
    (exf . ,(ly:make-pitch -1 2 Sixth-Flat))
    (eef . ,(ly:make-pitch -1 2 Eighth-Flat))
    (etf . ,(ly:make-pitch -1 2 Twelf-Flat))
    (e . ,(ly:make-pitch -1 2 Natural))
    (ets . ,(ly:make-pitch -1 2 Twelf-Sharp))
    (ees . ,(ly:make-pitch -1 2 Eighth-Sharp))
    (exs . ,(ly:make-pitch -1 2 Sixth-Sharp))
    (eqs . ,(ly:make-pitch -1 2 Quarter-Sharp))
    (ers . ,(ly:make-pitch -1 2 Third-Sharp))
    (etes . ,(ly:make-pitch -1 2 Three-Eighth-Sharp))
    (efts . ,(ly:make-pitch -1 2 Five-Twelf-Sharp))
    (es . ,(ly:make-pitch -1 2 Sharp))
    (ests . ,(ly:make-pitch -1 2 STwelf-Sharp))
    (efes . ,(ly:make-pitch -1 2 Five-Eighth-Sharp))
    (etrs . ,(ly:make-pitch -1 2 Two-Third-Sharp))
    (etqs . ,(ly:make-pitch -1 2 Three-Quarter-Sharp))
    (efxs . ,(ly:make-pitch -1 2 Five-Sixth-Sharp))
    (eses . ,(ly:make-pitch -1 2 Seven-Eighth-Sharp))
    (eets . ,(ly:make-pitch -1 2 Eleven-Twelf-Sharp))
    (ess . ,(ly:make-pitch -1 2 Double-Sharp))

    (fff . ,(ly:make-pitch -1 3 Double-Flat))
    (fetf . ,(ly:make-pitch -1 3 Eleven-Twelf-Flat))
    (fsef . ,(ly:make-pitch -1 3 Seven-Eighth-Flat))
    (ffxf . ,(ly:make-pitch -1 3 Five-Sixth-Flat))
    (ftqf . ,(ly:make-pitch -1 3 Three-Quarter-Flat))
    (ftrf . ,(ly:make-pitch -1 3 Two-Third-Flat))
    (ffef . ,(ly:make-pitch -1 3 Five-Eighth-Flat))
    (fstf . ,(ly:make-pitch -1 3 STwelf-Flat))
    (ff . ,(ly:make-pitch -1 3 Flat))
    (fftf . ,(ly:make-pitch -1 3 Five-Twelf-Flat))
    (ftef . ,(ly:make-pitch -1 3 Three-Eighth-Flat))
    (frf . ,(ly:make-pitch -1 3 Third-Flat))
    (fqf . ,(ly:make-pitch -1 3 Quarter-Flat))
    (fxf . ,(ly:make-pitch -1 3 Sixth-Flat))
    (fef . ,(ly:make-pitch -1 3 Eighth-Flat))
    (ftf . ,(ly:make-pitch -1 3 Twelf-Flat))
    (f . ,(ly:make-pitch -1 3 Natural))
    (fts . ,(ly:make-pitch -1 3 Twelf-Sharp))
    (fes . ,(ly:make-pitch -1 3 Eighth-Sharp))
    (fxs . ,(ly:make-pitch -1 3 Sixth-Sharp))
    (fqs . ,(ly:make-pitch -1 3 Quarter-Sharp))
    (frs . ,(ly:make-pitch -1 3 Third-Sharp))
    (ftes . ,(ly:make-pitch -1 3 Three-Eighth-Sharp))
    (ffts . ,(ly:make-pitch -1 3 Five-Twelf-Sharp))
    (fs . ,(ly:make-pitch -1 3 Sharp))
    (fsts . ,(ly:make-pitch -1 3 STwelf-Sharp))
    (ffes . ,(ly:make-pitch -1 3 Five-Eighth-Sharp))
    (ftrs . ,(ly:make-pitch -1 3 Two-Third-Sharp))
    (ftqs . ,(ly:make-pitch -1 3 Three-Quarter-Sharp))
    (ffxs . ,(ly:make-pitch -1 3 Five-Sixth-Sharp))
    (fses . ,(ly:make-pitch -1 3 Seven-Eighth-Sharp))
    (fets . ,(ly:make-pitch -1 3 Eleven-Twelf-Sharp))
    (fss . ,(ly:make-pitch -1 3 Double-Sharp))

    (gff . ,(ly:make-pitch -1 4 Double-Flat))
    (getf . ,(ly:make-pitch -1 4 Eleven-Twelf-Flat))
    (gsef . ,(ly:make-pitch -1 4 Seven-Eighth-Flat))
    (gfxf . ,(ly:make-pitch -1 4 Five-Sixth-Flat))
    (gtqf . ,(ly:make-pitch -1 4 Three-Quarter-Flat))
    (gtrf . ,(ly:make-pitch -1 4 Two-Third-Flat))
    (gfef . ,(ly:make-pitch -1 4 Five-Eighth-Flat))
    (gstf . ,(ly:make-pitch -1 4 STwelf-Flat))
    (gf . ,(ly:make-pitch -1 4 Flat))
    (gftf . ,(ly:make-pitch -1 4 Five-Twelf-Flat))
    (gtef . ,(ly:make-pitch -1 4 Three-Eighth-Flat))
    (grf . ,(ly:make-pitch -1 4 Third-Flat))
    (gqf . ,(ly:make-pitch -1 4 Quarter-Flat))
    (gxf . ,(ly:make-pitch -1 4 Sixth-Flat))
    (gef . ,(ly:make-pitch -1 4 Eighth-Flat))
    (gtf . ,(ly:make-pitch -1 4 Twelf-Flat))
    (g . ,(ly:make-pitch -1 4 Natural))
    (gts . ,(ly:make-pitch -1 4 Twelf-Sharp))
    (ges . ,(ly:make-pitch -1 4 Eighth-Sharp))
    (gxs . ,(ly:make-pitch -1 4 Sixth-Sharp))
    (gqs . ,(ly:make-pitch -1 4 Quarter-Sharp))
    (grs . ,(ly:make-pitch -1 4 Third-Sharp))
    (gtes . ,(ly:make-pitch -1 4 Three-Eighth-Sharp))
    (gfts . ,(ly:make-pitch -1 4 Five-Twelf-Sharp))
    (gs . ,(ly:make-pitch -1 4 Sharp))
    (gsts . ,(ly:make-pitch -1 4 STwelf-Sharp))
    (gfes . ,(ly:make-pitch -1 4 Five-Eighth-Sharp))
    (gtrs . ,(ly:make-pitch -1 4 Two-Third-Sharp))
    (gtqs . ,(ly:make-pitch -1 4 Three-Quarter-Sharp))
    (gfxs . ,(ly:make-pitch -1 4 Five-Sixth-Sharp))
    (gses . ,(ly:make-pitch -1 4 Seven-Eighth-Sharp))
    (gets . ,(ly:make-pitch -1 4 Eleven-Twelf-Sharp))
    (gss . ,(ly:make-pitch -1 4 Double-Sharp))

    (aff . ,(ly:make-pitch -1 5 Double-Flat))
    (aetf . ,(ly:make-pitch -1 5 Eleven-Twelf-Flat))
    (asef . ,(ly:make-pitch -1 5 Seven-Eighth-Flat))
    (afxf . ,(ly:make-pitch -1 5 Five-Sixth-Flat))
    (atqf . ,(ly:make-pitch -1 5 Three-Quarter-Flat))
    (atrf . ,(ly:make-pitch -1 5 Two-Third-Flat))
    (afef . ,(ly:make-pitch -1 5 Five-Eighth-Flat))
    (astf . ,(ly:make-pitch -1 5 STwelf-Flat))
    (af . ,(ly:make-pitch -1 5 Flat))
    (aftf . ,(ly:make-pitch -1 5 Five-Twelf-Flat))
    (atef . ,(ly:make-pitch -1 5 Three-Eighth-Flat))
    (arf . ,(ly:make-pitch -1 5 Third-Flat))
    (aqf . ,(ly:make-pitch -1 5 Quarter-Flat))
    (axf . ,(ly:make-pitch -1 5 Sixth-Flat))
    (aef . ,(ly:make-pitch -1 5 Eighth-Flat))
    (atf . ,(ly:make-pitch -1 5 Twelf-Flat))
    (a . ,(ly:make-pitch -1 5 Natural))
    (ats . ,(ly:make-pitch -1 5 Twelf-Sharp))
    (aes . ,(ly:make-pitch -1 5 Eighth-Sharp))
    (axs . ,(ly:make-pitch -1 5 Sixth-Sharp))
    (aqs . ,(ly:make-pitch -1 5 Quarter-Sharp))
    (ars . ,(ly:make-pitch -1 5 Third-Sharp))
    (ates . ,(ly:make-pitch -1 5 Three-Eighth-Sharp))
    (afts . ,(ly:make-pitch -1 5 Five-Twelf-Sharp))
    (as . ,(ly:make-pitch -1 5 Sharp))
    (asts . ,(ly:make-pitch -1 5 STwelf-Sharp))
    (afes . ,(ly:make-pitch -1 5 Five-Eighth-Sharp))
    (atrs . ,(ly:make-pitch -1 5 Two-Third-Sharp))
    (atqs . ,(ly:make-pitch -1 5 Three-Quarter-Sharp))
    (afxs . ,(ly:make-pitch -1 5 Five-Sixth-Sharp))
    (ases . ,(ly:make-pitch -1 5 Seven-Eighth-Sharp))
    (aets . ,(ly:make-pitch -1 5 Eleven-Twelf-Sharp))
    (ass . ,(ly:make-pitch -1 5 Double-Sharp))

    (bff . ,(ly:make-pitch -1 6 Double-Flat))
    (betf . ,(ly:make-pitch -1 6 Eleven-Twelf-Flat))
    (bsef . ,(ly:make-pitch -1 6 Seven-Eighth-Flat))
    (bfxf . ,(ly:make-pitch -1 6 Five-Sixth-Flat))
    (btqf . ,(ly:make-pitch -1 6 Three-Quarter-Flat))
    (btrf . ,(ly:make-pitch -1 6 Two-Third-Flat))
    (bfef . ,(ly:make-pitch -1 6 Five-Eighth-Flat))
    (bstf . ,(ly:make-pitch -1 6 STwelf-Flat))
    (bf . ,(ly:make-pitch -1 6 Flat))
    (bftf . ,(ly:make-pitch -1 6 Five-Twelf-Flat))
    (btef . ,(ly:make-pitch -1 6 Three-Eighth-Flat))
    (brf . ,(ly:make-pitch -1 6 Third-Flat))
    (bqf . ,(ly:make-pitch -1 6 Quarter-Flat))
    (bxf . ,(ly:make-pitch -1 6 Sixth-Flat))
    (bef . ,(ly:make-pitch -1 6 Eighth-Flat))
    (btf . ,(ly:make-pitch -1 6 Twelf-Flat))
    (b . ,(ly:make-pitch -1 6 Natural))
    (bts . ,(ly:make-pitch -1 6 Twelf-Sharp))
    (bes . ,(ly:make-pitch -1 6 Eighth-Sharp))
    (bxs . ,(ly:make-pitch -1 6 Sixth-Sharp))
    (bqs . ,(ly:make-pitch -1 6 Quarter-Sharp))
    (brs . ,(ly:make-pitch -1 6 Third-Sharp))
    (btes . ,(ly:make-pitch -1 6 Three-Eighth-Sharp))
    (bfts . ,(ly:make-pitch -1 6 Five-Twelf-Sharp))
    (bs . ,(ly:make-pitch -1 6 Sharp))
    (bsts . ,(ly:make-pitch -1 6 STwelf-Sharp))
    (bfes . ,(ly:make-pitch -1 6 Five-Eighth-Sharp))
    (btrs . ,(ly:make-pitch -1 6 Two-Third-Sharp))
    (btqs . ,(ly:make-pitch -1 6 Three-Quarter-Sharp))
    (bfxs . ,(ly:make-pitch -1 6 Five-Sixth-Sharp))
    (bses . ,(ly:make-pitch -1 6 Seven-Eighth-Sharp))
    (bets . ,(ly:make-pitch -1 6 Eleven-Twelf-Sharp))
    (bss . ,(ly:make-pitch -1 6 Double-Sharp))
    )

pitchnames = \newPitchNames
#(ly:parser-set-note-names pitchnames)

accidentalGlyphs = #`(
    (,Double-Sharp . "accidentals.doublesharp")
    (,Eleven-Twelf-Sharp . "noteheads.s0cross")
    (,Seven-Eighth-Sharp . "noteheads.s0cross")
    (,Five-Sixth-Sharp . "noteheads.s0cross")
    (,Three-Quarter-Sharp . "accidentals.sharp.slashslash.stemstemstem")
    (,Two-Third-Sharp . "noteheads.s0cross")
    (,Five-Eighth-Sharp . "accidentals.sharp.arrowup")
    (,STwelf-Sharp . "noteheads.s0cross")
    (,Sharp . "accidentals.sharp")
    (,Five-Twelf-Sharp . "noteheads.s0cross")
    (,Three-Eighth-Sharp . "accidentals.sharp.arrowdown")
    (,Third-Sharp . "noteheads.s0cross")
    (,Quarter-Sharp . "accidentals.sharp.slashslash.stem")
    (,Sixth-Sharp . "noteheads.s0cross")
    (,Eighth-Sharp . "accidentals.natural.arrowup")
    (,Twelf-Sharp . "noteheads.s0cross")
    (,Natural . "accidentals.natural")
    (,Twelf-Flat . "noteheads.s0cross")
    (,Eighth-Flat . "accidentals.natural.arrowdown")
    (,Sixth-Flat . "noteheads.s0cross")
    (,Quarter-Flat . "accidentals.mirroredflat")
    (,Third-Flat . "noteheads.s0cross")
    (,Three-Eighth-Flat . "accidentals.flat.arrowup")
    (,Five-Twelf-Flat . "noteheads.s0cross")
    (,Flat . "accidentals.flat")
    (,STwelf-Flat . "noteheads.s0cross")
    (,Five-Eighth-Flat . "accidentals.flat.arrowdown")
    (,Two-Third-Flat . "noteheads.s0cross")
    (,Three-Quarter-Flat . "accidentals.mirroredflat.flat")
    (,Five-Sixth-Flat . "noteheads.s0cross")
    (,Seven-Eighth-Flat . "noteheads.s0cross")
    (,Eleven-Twelf-Flat . "noteheads.s0cross")
    (,Double-Flat . "accidentals.flatflat")
)

\layout {
    \accidentalStyle forget
    \context {
        \Score
        \override KeySignature.glyph-name-alist = \accidentalGlyphs
        \override Accidental.glyph-name-alist = \accidentalGlyphs
        \override AccidentalCautionary.glyph-name-alist = \accidentalGlyphs
        \override TrillPitchAccidental.glyph-name-alist = \accidentalGlyphs
        \override AmbitusAccidental.glyph-name-alist = \accidentalGlyphs
    }
}

\score {
    <<
        \new Staff {
            \new Voice {
                cff'4
				\eleven-twelfs-flat
                cetf'4
				\seven-eighths-flat
                csef'4
				\five-sixths-flat
                cfxf'4
                ctqf'4
				\two-thirds-flat
                ctrf'4
				\five-eighths-flat
                cfef'4
				\seven-twelfs-flat
                cstf'4
                cf'4
				\five-twelfs-flat
                cftf'4
                \three-eighths-flat
                ctef'4
				\one-third-flat
                crf'4
                cqf'4
				\one-sixth-flat
                cxf'4
                \one-eighth-flat
                cef'4
				\one-twelf-flat
                ctf'4
                c'4
				\one-twelf-sharp
                cts'4
                \one-eighth-sharp
                ces'4
                \one-sixth-sharp
                cxs'4
                cqs'4
                \one-third-sharp
                crs'4
                \three-eighths-sharp
                ctes'4
				\five-twelfs-sharp
                cfts'4
                cs'4
				\seven-twelfs-sharp
                csts'4
                \five-eighths-sharp
                cfes'4
                \two-thirds-sharp
                ctrs'4
                ctqs'4
                \five-sixths-sharp
                cfxs'4
                \seven-eighths-sharp
                cses'4
				\eleven-twelfs-sharp
                cets'4
                css'4
            }
        }
    >>
}
