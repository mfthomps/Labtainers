#network.eps generated from network.fig by the xfig program
#DO NOT REMOVE network.fig and network.eps

ssh-tunnel.pdf: ssh-tunnel.tex header.tex network.eps
	pdflatex -jobname=ssh-tunnel ssh-tunnel
	pdflatex -jobname=ssh-tunnel ssh-tunnel

clean:
	rm -fr auto
	rm -f ssh-tunnel.aux ssh-tunnel.log ssh-tunnel.out ssh-tunnel.pdf
