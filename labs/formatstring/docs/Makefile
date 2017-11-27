formatstring.pdf: Format_String.tex
	latex Format_String
	pdflatex -jobname=formatstring Format_String
	pdflatex -jobname=formatstring Format_String

clean:
	rm -fr auto
	rm -f Format_String.aux Format_String.log Format_String.pdf
