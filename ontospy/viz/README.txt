To add a new viz

- add .py file
- add .html template
- update catalogue in __init__.py

eg
from .viz_d3packhierarchy import run as funX

VISUALIZATIONS_LIST += [("Pack Hierarchy (interactive / experimental)", fun3)]