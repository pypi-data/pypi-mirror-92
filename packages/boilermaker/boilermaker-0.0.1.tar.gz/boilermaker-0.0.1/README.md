# boilermaker

A C++ code generator that transforms a declarative description into static types.

The generated code has selectable features, such as serialization, deserialization, and reasoning about comparisons. You can define data types, and use most STL classes as well to aggregate an expressive static hierarchy, and rapidly change the declarations to modify swaths of C++ code.

The tool can be configured to read C-style and C++-style enumerations from headers, for use in the declarations as well.

Useful for rapidly generating C++ code that can read configuration files, and other data files in [Humon|https://github.com/spacemeat/humon] format. Usage docs coming eventually. Boilermaker can create header-only style C++, or headers and translations units, and emplace code directly into your project. Simply #include the main header in your project, and call the generated functions to create and load the complex types. All the generated code is readable, as you might write it, and you're encouraged to see what it's making.


# installing boilermaker
```bash
$ pip install boilermaker
```

## Usage

No info yet. This is a very nascent project.

# Developing hboilermaker

To install boilermaker and the tools needed to develop and run tests, run the following:

```bash
$ pip install -e .[dev]
```
