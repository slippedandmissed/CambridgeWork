all: phase_1.pdf \
	 phase_2.pdf \
	 phase_3_with_cover_sheet.pdf \
	 mapping_from_discrete_to_continuous_tsp.pdf

%.pdf : %.md
	pandoc $< -o $@

%.pdf : %.Rmd
	echo "library(rmarkdown)\nrender(\"$<\")" | R --no-save

%_with_cover_sheet.pdf : %.pdf
	gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dAutoRotatePages=/None -sOutputFile=$@  ./assets/cover_sheet.pdf $<

clean:
	rm *.pdf