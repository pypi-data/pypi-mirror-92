# Pytransformation
![main](https://github.com/Dyfox100/pytransformation/workflows/Run%20Tests/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/Dyfox100/pytransformation/branch/main/graph/badge.svg?token=Z45U2F27QV)](https://codecov.io/gh/Dyfox100/pytransformation)

Pytransformation is a library to perform various source code transformations on Python code. It may be useful in cross-compilation projects. It includes both a script that can transform source code files, and an Python 3 API that can be used independently.

## Transformations Available

#### Converting For Loops to While Loops
Pytransformation can convert all for loops in Python source code to While loops. The only restrictions are that the iterator in the for loop must be indexable. See below: 

Input             |  Output
:-------------------------:|:-------------------------:
![](https://github.com/Dyfox100/pytransformation/blob/main/example_photos/for2while_input.png)  |  ![](https://github.com/Dyfox100/pytransformation/blob/main/example_photos/for2while_output.png)

#### Moving First Use of Variables to the Top of Scope
Pytransformation also supports moving the first use of variables to the top of the scope they exist in. This eliminates variable declaration hoisting. See below:

Input             |  Output
:-------------------------:|:-------------------------:
![](https://github.com/Dyfox100/pytransformation/blob/main/example_photos/move_var_decls_input.png)  |  ![](https://github.com/Dyfox100/pytransformation/blob/main/example_photos/move_var_decls_output.png)
#### Naming Function Applications
Pytransformation can name un-nammed function applications. This will name all function applications irregardless of where they exist. Nested function applications will be pulled out and named. See below:

Input             |  Output
:-------------------------:|:-------------------------:
![](https://github.com/Dyfox100/pytransformation/blob/main/example_photos/name_func_apps_input.png)  |  ![](https://github.com/Dyfox100/pytransformation/blob/main/example_photos/name_func_outputs.png)

## Usage
#### As a script
To run pytransformation, simply navigate to the top level directory and run the `pytransformation.py` script. This takes input and output file arguments, along with the transformations to be performed. For example: 

`./pytransformation.py file_to_transform.py output_file.py -all`

The arguments used to specify which transformations to perform are `-for2while`, `-name_apps`, `-move_var_decls`, and `-all`. Either a file path or a path to a directory can be specified in the input/output file arguments. If a directory is specified, it will transform all `.py` files in the directory. 
#### Python API
The python API supports transforming both strings and files. If you wish to transform strings use the `String_Transformer` class. If you wish to transform files, use the `File_Transformer` class. The two classes have identical apis, except the `File_Transformer` takes an input and output file name (and writes to the output file), while the `String_Transformer` takes a string and returns a string.  Transformations should be supplied to the transformers using a list of transformations found in the enumerated class `Transformations`. See example below:
```
from pytransformation import String_Transformer
from pytransformation import Transformations

# Assume the variable src has a string of source code in it.

transformations = [
        Transformations.MAKE_FOR_LOOPS_WHILE,
        Transformations.MOVE_DECLS_TO_TOP_OF_SCOPE,
        Transformations.NAME_ALL_FUNCTION_APPLICATIONS,
    ]
    
transformer = String_Transformer(transformations)
new_src = transformer.transform(src)

```

## Contributing
Contributions are welcome. See the issues list for a few ideas of potential contributions. To develop on pytransformation please install the pre-commit hook by running `pre-commit install` after downloading the source. This will install a pre-commit hook that runs the flake8 linter, to ensure code is more or less PEP 8 formatted. To run tests simply run `pytest` in the top level directory (or in the tests directory). The test suite uses input and output files in the `test_files` directory. If new tests rely on a piece of sorce code to test, the source code and expected result should be added in .py files in the `test_files` directory, not written inline in the test file. Then the test file should go in the top of the `tests` directory. There is a script to create new test files with the correct directory structure. Run `./make_new_tests <name_of_test>` in the `tests` directory.

