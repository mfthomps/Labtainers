buf64.pdf: buf64.tex header.tex
	latex buf64
	pdflatex -jobname=buf64 buf64
	pdflatex -jobname=buf64 buf64

clean:
	rm -fr auto
	rm -f *.aux *.log *.pdf *.dvi *.out
