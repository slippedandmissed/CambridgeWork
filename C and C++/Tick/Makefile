summary:
	make pcolparse
	g++ -std=c++11 -Wall --pedantic -o summary pcolparse.o summary.cc

extract:
	make pcolparse
	g++ -std=c++11 -Wall --pedantic -o extract pcolparse.o extract.cc

pcolparse:
	g++ -std=c++11 -Wall --pedantic -c pcolparse.cc

clean:
	rm -f pcolparse.o
	rm -f summary
	rm -f extract