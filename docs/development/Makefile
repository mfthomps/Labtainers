all: development.pdf imodules.pdf
development.pdf: development.tex
	pdflatex development
	pdflatex development
imodules.pdf: imodules.tex
	latex imodules
	pdflatex imodules
clean:
	rm -fr auto
	rm -fr development.aux development.pdf
