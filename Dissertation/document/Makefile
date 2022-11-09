SRC_DIR=latex
OUT_DIR=out
OUT_DIR_FROM_SRC_DIR=$(shell realpath --relative-to "$(SRC_DIR)" "$(OUT_DIR)")
ENTRYPOINT=Dissertation
WORD_COUNT_OUTPUT_FILE=$(SRC_DIR)/wordcount.autogen.tex
WORD_COUNTABLE_FILES=introduction.tex preparation.tex implementation.tex evaluation.tex conclusions.tex 

all: $(OUT_DIR)/$(ENTRYPOINT).pdf

force: clean all

output-dir:
	mkdir -p $(OUT_DIR)

word-count:
	echo "\nPerforming word count"; \
	sum=0; \
	for file in $(WORD_COUNTABLE_FILES) ; do \
		n=$$(detex $(SRC_DIR)/$$file | tr -cd '0-9A-Za-z \n' | wc -w); \
		echo "$$n  ---  $(SRC_DIR)/$$file"; \
		sum=$$(expr $$sum + $$n); \
	done; \
	echo "\n\e[0;32mTotal word count:\e[0m $$sum\n"; \
	echo "Writing into $(WORD_COUNT_OUTPUT_FILE)"; \
	echo -n "$$sum" > $(WORD_COUNT_OUTPUT_FILE)

$(OUT_DIR)/%.pdf: word-count \
									$(SRC_DIR)/%.tex \
									output-dir
	cd $(SRC_DIR) && xelatex -output-directory $(OUT_DIR_FROM_SRC_DIR) $*.tex
	cp $(SRC_DIR)/*.bib $(OUT_DIR)/
	cd $(OUT_DIR) && biber $*
	cp $(OUT_DIR)/Dissertation.idx $(SRC_DIR)/
	cd $(SRC_DIR) && xelatex -output-directory $(OUT_DIR_FROM_SRC_DIR) $*.tex
	cd $(SRC_DIR) && xelatex -output-directory $(OUT_DIR_FROM_SRC_DIR) $*.tex
	rm $(SRC_DIR)/Dissertation.idx
	rm $(SRC_DIR)/Dissertation.ilg
	rm $(SRC_DIR)/Dissertation.ind

clean:
	rm -rf $(OUT_DIR)
	rm -f $(WORD_COUNT_OUTPUT_FILE)