# sphinx-multiversion

Fork of https://github.com/Holzhaus/sphinx-multiversion for the Scylla Project.

Sphinx extension for building self-hosted versioned docs.

Original documentation can be found at: https://holzhaus.github.io/sphinx-multiversion/

## Fork additions

### Prebuild command

The fork introduces the possibility to run custom commands before building the docs with the option ``--pre-build``.

This could be useful to prepare the docs repository before running ``sphinx-build``, debug the execution, or even generate versioned documentation using other builders.

For example, imagine that you want to build versioned docs written in Sphinx, but the API reference is generated with JavaDoc. This option enables the generation of both versioned docs to host them under the same folder using GitHub Pages.

Here's an example showing the directory where the build command is running:

```
sphinx-multiversion docs build/html --pre-build pwd
```

You can pass multiple commands by adding extra ``--pre-build`` tags. The commands run in order, from left to right:

```
sphinx-multiversion docs build/html --pre-build pwd --pre-build ls
```

### Rename latest version URL

The ``smv_latest_version`` setting determines which is the latest version.
Setting this option could be useful to show a warning when users are not reading the latest version.

You can override the latest version output directory with ``smv_rename_latest_version``.

Here's an example:

```
smv_latest_version = 'x.y.z'        # Use the branch/tag name
smv_rename_latest_version = 'latest' # Use the commit hash
```

## Maintenance

This fork will be maintained until https://github.com/Holzhaus/sphinx-multiversion/issues/45 is solved.
