import json
import os

from typing import List

from voxility_pro.utils.file_utils import get_addon_root_dir

LANG: str = 'en'
loaded_translations: List = None

def load_translations(language: str) -> None:
    translations_folder = os.path.join(get_addon_root_dir(), "languages")
    translations_file = os.path.join(translations_folder, f"{language}.json")
    
    with open(translations_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_translation(key: str):
    k: str = loaded_translations.get(key, key)
    return k

def register():
    global loaded_translations
    loaded_translations = load_translations(LANG)

def unregister():
    global loaded_translations
    loaded_translations = None



