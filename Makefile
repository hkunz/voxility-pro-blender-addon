.PHONY: all clean operators

all:

vox-operators:
	@echo "Generating supported-formats json file..."
	./scripts/generate-supported-formats-json.sh
	@echo "Generating operators..."
	./scripts/generate-op-exporter.sh --all

create-next-tag:
	./scripts/create-tag.sh -i

zip:
	./scripts/build.sh

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
