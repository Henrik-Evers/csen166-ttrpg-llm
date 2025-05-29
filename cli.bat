:: Builds a new model based on Modelfiles, then runs app.py.

ollama create app-model -f ./Modelfile-Main
ollama create app-charsheet-reader -f ./Modelfile-Processing
py app.py
