# Ollama

If you want to update the models that are served with ollama, update the Config Map `ollama-models-config`.

## Currently Deployed Default Models

- llama3.1:8b
- granite3.3:8b

## Ollama Model Viewer

An instance of the [Ollama Model Viewer](https://github.com/redhat-ai-dev/ollama-model-viewer) is deployed in the same namespace as Ollama, providing a basic UI to view deployed models and see GPU usage.
