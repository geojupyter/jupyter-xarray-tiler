# Develop

Double-check the server extension is properly installed:

```bash
uv run jupyter server extension list
```

Start JupyterLab:

```bash
uv run jupyter lab
```

Remember that changes won't immediately be reflected in the running instance of
JupyterLab.
Depending on what you've changed, you may need to restart the server (CTRL+C and start
JupyterLab again), or restart the kernel in the JupyterLab UI.

You can use notebooks in the `examples/` directory as a starting point for interactively
testing your development build.
