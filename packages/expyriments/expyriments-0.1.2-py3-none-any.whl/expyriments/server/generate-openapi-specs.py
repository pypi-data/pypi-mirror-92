import json
import sys
from pathlib import Path

# Standalone boilerplate before relative imports
if __package__ is None:
    DIR = Path(__file__).resolve().parent
    sys.path.insert(0, str(DIR.parent))
    __package__ = DIR.name

from .api import api_app

# write openapi.json spec to file
with open("./openapi.json", "w") as outfile:
    print("Create API docs", api_app.openapi())
    json.dump(api_app.openapi(), outfile)
