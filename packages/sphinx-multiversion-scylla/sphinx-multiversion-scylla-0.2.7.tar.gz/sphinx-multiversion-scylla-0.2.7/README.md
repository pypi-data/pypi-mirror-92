# sphinx-multiversion

Fork of https://github.com/Holzhaus/sphinx-multiversion for the Scylla Project.

Sphinx extension for building self-hosted versioned docs.

This extension aims to provide a clean implementation that tries to avoid
messing with Sphinx internals as much as possible.

Documentation can be found at: https://holzhaus.github.io/sphinx-multiversion/

## Fork changes

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

## Maintenance

This fork will be maintained until https://github.com/Holzhaus/sphinx-multiversion/issues/45 is solved.