Convenience functions related to modules and importing.

*Latest release 20210123*:
module_attributes: skip values from other modules _if we know the module_ (computed values like tuples have no module and still need to be returned).

## Function `direct_imports(src_filename, module_name=None)`

Crudely parse `src_filename` for `import` statements.
Return the set of directly imported module names.

If `module_name` is not `None`,
resolve relative imports against it.
Otherwise, relative import names are returned unresolved.

This is a very simple minded source parse.

## Function `import_module_from_file(module_name, source_file, sys_path=None)`

Import a specific file as a module instance,
return the module instance.

Parameters:
* `module_name`: the name to assign to the module
* `source_file`: the source file to load
* `sys_path`: optional list of paths to set as `sys.path`
  for the duration of this import;
  the default is the current value of `sys.path`

Note that this is a "bare" import;
the module instance is not inserted into `sys.modules`.

*Warning*: `sys.path` is modified for the duration of this function,
which may affect multithreaded applications.

## Function `import_module_name(module_name, name, path=None, lock=None)`

Import `module_name` and return the value of `name` within it.

Parameters:
* `module_name`: the module name to import.
* `name`: the name within the module whose value is returned;
  if `name` is `None`, return the module itself.
* `path`: an array of paths to use as sys.path during the import.
* `lock`: a lock to hold during the import (recommended).

## Function `module_attributes(M)`

Generator yielding the names and values of attributes from a module
which were defined in the module.

## Function `module_files(M)`

Generator yielding `.py` pathnames involved in a module.

## Function `module_names(M)`

Return a list of the names of attributes from a module which were
defined in the module.

# Release Log



*Release 20210123*:
module_attributes: skip values from other modules _if we know the module_ (computed values like tuples have no module and still need to be returned).

*Release 20200521*:
* New import_module_from_file function to import a Python file as a module instance.
* New direct_imports(src_filename,module_name=None) returning the set of directly imports module names.

*Release 20190101*:
New functions: module_names, module_attributes.

*Release 20160918*:
* New generator function module_files yielding pathnames.
* import_module_name: accept name=None, just return the module.
* Add empty "install_requires" for DISTINFO completeness.

*Release 20150116*:
Initial PyPI release.
