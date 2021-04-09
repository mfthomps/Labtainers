gdb-cpp.pdf: gdb-cpp.tex header.tex
	latex gdb-cpp
	pdflatex -jobname=gdb-cpp gdb-cpp
	pdflatex -jobname=gdb-cpp gdb-cpp

clean:
	rm -fr auto
	rm -f *.aux *.log *.pdf *.dvi *.out
