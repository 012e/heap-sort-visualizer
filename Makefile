default: build

clean:
	rm ./output/* -f

preview:
	imv ./output/*.svg

d2:
	@echo "Exporting d2 files"
	python heap_visualizer.py

svg: d2
	@echo "converting d2 files to SVGs"
	parallel d2 ::: ./output/*.d2

png: svg
	@echo "Converting SVGs to PNGs"
	convert ./output/*.svg output/heapify-%02d.png

mp4: clean png
	ffmpeg -framerate 1 -i ./output/heapify-%02d.png -c:v libx264 -r 30 -pix_fmt yuv420p output/heapify.mp4

build: clean png
