.PHONY: all clean operators

all: \
	clean \
	vox-support-formats \
	vox-operators \
	vox-menus \
	vox-addon-preferences

vox-support-formats:
	@echo "=====================================================================================>"
	@echo "Generating supported-formats json file ..."
	./scripts/generate-supported-formats-json.sh

vox-operators:
	@echo "=====================================================================================>"
	@echo "Generating operators ..."
	./scripts/generate-op-exporter.sh --all

vox-menus:
	@echo "=====================================================================================>"
	@echo "Generating voxel submenu files ..."
	./scripts/generate-vox-menu-py-file.sh import
	./scripts/generate-vox-menu-py-file.sh export

vox-addon-preferences:
	@echo "=====================================================================================>"
	@echo "Generating AddonPreferences file ..."
	./scripts/generate-addon-preferences-file.sh

vox-documentation-content-final:
	@echo "=====================================================================================>"
	@echo "Generating voxility documentation content file ..."
	./scripts/generate-documentation-content-html.sh

create-next-tag:
	@echo "=====================================================================================>"
	@echo "Create new tag ..."
	./scripts/create-tag.sh -i

zip:
	./scripts/build.sh

fix-py-permissions:
	find . -type f -name '*.py' -exec chmod 755 {} +

clean:
	@echo "=====================================================================================>"
	@echo "Cleaning ..."
	find . -type d -name '__pycache__' -exec rm -r {} +
