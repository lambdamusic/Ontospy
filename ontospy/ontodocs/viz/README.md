### How To add a new viz

-   add .py file named as 'viz\_%s'
-   add .html templates (if in new folder, updated also settings.TEMPLATES in builder.py)
-   update catalogue in `CONFIG.py`

### Testing locally

-   `python -m ontospy.ontodocs.viz.viz_d3barHierarchy` picks a random ontology and runs the script
