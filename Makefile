.PHONY: all clean operators

all:

vox-operators:
	@echo "Generating operators..."
	./generate-op-exporter.sh --all

create-next-tag:
	./create-tag.sh -i

zip:
	./build.sh

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
