all: Supervision_1.pdf

trees/%.png: assets/%.tree
	../../generate_proof_tree.py $< -o $@

Supervision_1.md : trees/1.3a.png \
									 trees/1.3b.png

%.pdf : %.md
	pandoc $< -o $@

clean:
	rm -f *.pdf
	rm -f trees/*.png