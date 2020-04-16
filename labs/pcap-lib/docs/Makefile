pcap-lib.pdf: pcap-lib.tex header.tex
	latex pcap-lib
	pdflatex -jobname=pcap-lib pcap-lib
	pdflatex -jobname=pcap-lib pcap-lib

clean:
	rm -fr auto
	rm -f pcap-lib.aux pcap-lib.log pcap-lib.pdf pcap-lib.dvi pcap-lib.out
