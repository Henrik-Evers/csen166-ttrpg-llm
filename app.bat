:: Builds a new model based on Modelfile, then runs the application with a GUI.

ollama create app-model -f ./Modelfile-Main
ollama create app-charsheet-reader -f ./Modelfile-Processing
py gui.py
