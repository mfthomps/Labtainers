remote-dns.pdf: DNS_Remote.tex header.tex
	latex DNS_Remote
	pdflatex -jobname=remote-dns DNS_Remote
	pdflatex -jobname=remote-dns DNS_Remote

clean:
	rm -fr auto
	rm -f *.aux *.log *.pdf *.out
