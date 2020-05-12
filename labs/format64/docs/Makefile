format64.pdf: format64.tex header.tex
	latex format64
	pdflatex -jobname=format64 format64
	pdflatex -jobname=format64 format64

clean:
	rm -fr auto
	rm -f *.aux *.log *.pdf *.dvi *.out
