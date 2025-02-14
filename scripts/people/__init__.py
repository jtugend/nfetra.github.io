import os
from pathlib import Path
import random
from textwrap import dedent

import yaml

from sphinx.application import Sphinx
from sphinx.util import logging

LOGGER = logging.getLogger("conf")

def build_teamgallery(app: Sphinx):
    # Build the gallery file
    LOGGER.info("building gallery...")
    grid_items = []
    projects = yaml.safe_load((Path(app.srcdir) / "configs/team.yml").read_text())
    random.shuffle(projects)
    for item in projects:
        if not item.get("image"):
            item["image"] = "https://unisvalbard.github.io/AG222/_static/UNIS_logo.gif"
        
        LOGGER.info(f"test_{item}")


        if not item.get("keywords"):
            item["keywords"] = ""

    # change padding when more than 2 people
        grid_items.append(
f"""\
`````{{grid-item-card}}
:text-align: left
```{{image}} {item["image"]}
:width: 150px
:align: right
```
**{item["name"]} {item["surname"]}**{", " + item["title"] if item["title"] else ""}{" - " + "*" + item["projectPI"] + "*" if "projectPI" in item.keys() else ""}<br>{item["companytitle"]}


{{bdg-link-secondary}}`linkedin <{item["linkedin"]}>`


{item["bio"]}
`````
"""
        )
    grid_items = "\n".join(grid_items)

# :column: text-center col-6 col-lg-4
# :card: +my-2
# :img-top-cls: w-75 m-auto p-2
# :body: d-none

# change padding when more than 2 people
    panels = f"""
``````{{grid}} 1 1 1 1
:gutter: 3
:padding: 1
:class-container: full-width
{dedent(grid_items)}
``````
    """
    (Path(app.srcdir) / "pages/team-gallery.txt").write_text(panels)