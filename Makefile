update:
	git pull
	git submodule update --remote coregraphene
	git submodule update --remote grapheneqtui

run:
	python3 app.py
