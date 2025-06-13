# llama-stack

This ArgoCD application configures an instance of llama stack, pointing to the instance of Ollama deployed via this repository

## Prerequisites

Before deploying this application, a secret, `llama-stack-secret` must exist in the same namespace, with the following key-value pairs:

- `OLLAMA_URL`: The hostname of the Ollama instance
- `OLLAMA_API_TOKEN`: An API key used to access the Ollama instance (if needed)