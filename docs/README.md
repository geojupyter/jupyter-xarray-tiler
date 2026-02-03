# Documentation

Documentation is built and served by ReadTheDocs.

## Build the docs locally

You may want to test your changes locally before pushing.

```bash
uv run make html
```

If this build has a non-zero return code, the build has failed and so a deployment to
ReadTheDocs would also fail.
Check the error text in the output!
