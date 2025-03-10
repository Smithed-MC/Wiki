import json
from pathlib import Path

book_data = json.loads(Path("input/generated_pages_example.json").read_text())

book_pages = []
for page in book_data["pages"]:
    book_pages.append(page)

components = {
            "minecraft:written_book_content": {
              "pages": book_pages,
              "title": book_data.get("title", "Wiki Book"),
              "author": book_data.get("author", "smithed.wiki"),
              "generation": 2
            }
          }

components.update(book_data["components"])

book = {
  "pools": [
    {
      "rolls": 1,
      "entries": [
        {
          "type": "minecraft:item",
          "name": "minecraft:written_book"
        }
      ],
      "functions": [
        {
          "function": "minecraft:set_components",
          "components": components
        }
      ]
    }
  ]
}

def get_book():
    return book