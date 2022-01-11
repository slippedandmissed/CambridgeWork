summary:
	make pcolparse
	gcc -std=c11 -Wall -g --pedantic -o summary pcolparse.o summary.c

extract:
	make pcolparse
	g++ -std=c++11 -Wall --pedantic -o extract pcolparse.o extract.cc

pcolparse:
	gcc -std=c11 -g -Wall --pedantic -c pcolparse.c

clean:
	rm -f pcolparse.o
	rm -f summary
	rm -f extract