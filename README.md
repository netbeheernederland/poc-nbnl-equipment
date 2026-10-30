# PoC: NBNL Equipment

The entry point is the Jupyter Notebook: `src/nbnl-equipment.ipynb`.

Profile source files can be found under `src/`. Under `src/remote` you can find artifacts that should at some point become remote dependencies.

In order to run the notebook properly, make sure you:

* Build and post-process the necessary artifacts, most notablt converting YAML-LD to JSON-LD. This can be done from the notebook.
* Serve the built artifacts locally: `python -m http.server -d built`.
* Run the validation in the notebook.