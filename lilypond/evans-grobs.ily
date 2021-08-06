%%% blank time signature %%%

#(define ((blank-time-signature) grob)
   (grob-interpret-markup grob
          (markup #:override '(baseline-skip . 2.5) #:number
                  (#:line ((#:fontsize -3 #:column ("X" "X")))))))
