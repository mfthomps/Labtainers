packet-introspection.pdf: packet-introspection.tex header.tex
	latex packet-introspection
	pdflatex -jobname=packet-introspection packet-introspection
	pdflatex -jobname=packet-introspection packet-introspection

clean:
	rm -fr auto
	rm -f packet-introspection.aux packet-introspection.log packet-introspection.pdf packet-introspection.dvi packet-introspection.out
