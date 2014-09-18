all: pack

pack:
	cd src/ && zip -r ../lenovo-yoga-switcher.plasmoid .

install: pack
	plasmapkg -r lenovo-yoga-switcher || true
	plasmapkg -i lenovo-yoga-switcher.plasmoid
