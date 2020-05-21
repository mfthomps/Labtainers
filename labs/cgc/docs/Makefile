cgc.pdf: cgc.tex header.tex
	latex cgc
	pdflatex -jobname=cgc cgc
	pdflatex -jobname=cgc cgc

clean:
	rm -fr auto
	rm -f *.aux *.log *.pdf *.dvi *.out
