default: build

clean:
	rm ./output/* -f

preview:
	imv ./output/*.svg

d2:
	python heap_visualizer.py

svg: d2
	for file in ./output/*.d2; do \
		d2 "$$file"; \
	done

png: svg
	convert ./output/*.svg output/heapify-%02d.png

build: clean png preview
