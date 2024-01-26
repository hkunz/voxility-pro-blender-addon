.PHONY: all clean operators

all: \
	vox-support-formats \
	vox-operators \
	vox-menus

vox-support-formats:
	@echo "Generating supported-formats json file..."
	./scripts/generate-supported-formats-json.sh

vox-operators:
	@echo "Generating operators..."
	./scripts/generate-op-exporter.sh --all

vox-menus:
	@echo "Generating voxel submenu files..."
	./scripts/generate-vox-menu-py-file.sh import
	./scripts/generate-vox-menu-py-file.sh export

create-next-tag:
	./scripts/create-tag.sh -i

zip:
	./scripts/build.sh

fix-py-permissions:
	find . -type f -name '*.py' -exec chmod 755 {} +

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
