"""発信規格の単一ソース specs.json の読み込み口。各チェッカーは load() だけを使う。"""
import json, os
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "specs.json")
def load():
    with open(PATH, encoding="utf-8") as f:
        return json.load(f)
def image(fmt):
    return load()["image"][fmt]
def dims(fmt):
    s = image(fmt); return (s["w"], s["h"])
