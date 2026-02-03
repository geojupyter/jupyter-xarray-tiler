# Releasing a new version

Once you're ready to make a release, use the GitHub interface to create a new release
(and tag, if needed).

The package will only publish to PyPI once a GitHub Release has been created.

When creating a GitHub release:

* Ensure the `main` branch checks are all passing before proceeding.
* Follow [Semantic Versioning](https://semver.org/) to pick a tag for this release.
* **Do not prefix the tag with `v`**, i.e. use `0.1.0`, **not** `v0.1.0`.
* Use the automated "Generate release notes" feature in GitHub.
  **Clean it up!**
  Ensure the release notes are written for users (developers of Jupyter map libraries).
  Emphasize breaking changes in their own H2 section of the release notes.
  Remove "noise" changes, e.g. "Update pre-commit hooks" or "Add pull request template".

## Publishing to `conda-forge`

If the package is not on conda forge yet, check the documentation to learn how to add it: https://conda-forge.org/docs/maintainer/adding_pkgs.html

Otherwise a bot should pick up the new version publish to PyPI, and open a new PR on the
feedstock repository automatically.
Review the PR, updating dependencies if necessary, and merge.
