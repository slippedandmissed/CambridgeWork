SRC_DIR=latex
OUT_DIR=out
OUT_DIR_FROM_SRC_DIR=$(shell realpath --relative-to "$(SRC_DIR)" "$(OUT_DIR)")
ENTRYPOINT=Dissertation

all: $(OUT_DIR)/$(ENTRYPOINT).pdf

force: clean all

output-dir:
	mkdir -p $(OUT_DIR)

$(OUT_DIR)/%.pdf: $(SRC_DIR)/%.tex \
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
