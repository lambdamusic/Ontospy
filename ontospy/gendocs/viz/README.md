### How To add a new viz

-   add .py file named as 'viz\_%s'
-   add .html templates (if in new folder, updated also settings.TEMPLATES in builder.py)
-   update catalogue in `CONFIG.py`

### Testing locally

-   `python -m ontospy.gendocs.viz.viz_d3bar_hierarchy` picks a random ontology and runs the script
-   `python -m ontospy.gendocs.viz.viz_html_single` 