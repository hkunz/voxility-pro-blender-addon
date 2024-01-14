import json
import os

from vox_exporter import bl_info
from vox_exporter.utils import get_addon_root_dir

LANG = 'en'
loaded_translations = None

def load_translations(language):
    addon_name = bl_info["name"]
    translations_folder = os.path.join(get_addon_root_dir(), "languages")
    translations_file = os.path.join(translations_folder, f"{language}.json")
    
    with open(translations_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_translation(key):
    #global loaded_translations
    #if not loaded_translations:
    #    loaded_translations = load_translations(LANG)
    return loaded_translations.get(key, key)

def register_translations():
    global loaded_translations
    loaded_translations = load_translations(LANG)

def unregister_translations():
    pass



