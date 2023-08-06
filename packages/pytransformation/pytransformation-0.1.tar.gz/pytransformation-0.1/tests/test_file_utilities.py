import os


def get_all_test_and_result_files(dir_name):
    """Reads content of all test and result files in the directory at
    ./tet_files/<dir_name> into 2d array of strings. All files should be named
    test_<number> or result_<number>. Each test file should have a result file.
        Parameters:
            dir_name: name of directory in ./test_files
        Returns:
            2d array of strings with test and result file content.
    """
    absolute_path = os.path.dirname(os.path.realpath(__file__))
    absolute_path = os.path.join(absolute_path, "test_files", dir_name)
    file_names = [f for f in os.listdir(absolute_path)
                  if os.path.isfile(os.path.join(absolute_path, f))]
    test_files = filter(lambda f: "test" in f, file_names)

    def get_number_from_test_file(file_name):
        file_without_dot_py = file_name.split(".py")[0]
        file_without_test_prefix = file_without_dot_py.split("_")[1]
        return int(file_without_test_prefix)

    try:
        list_of_test_numbers = map(get_number_from_test_file, test_files)
    except ValueError as e:
        print("File Not Understood! Ensure that files are named test_<number>")
        raise(e)

    test_strings = []
    result_strings = []
    try:
        for test_num in sorted(list_of_test_numbers):
            test_file = "testcase_" + str(test_num) + ".py"
            result_file = "result_" + str(test_num) + ".py"

            files_to_close = []
            test = open(os.path.join(absolute_path, test_file), "r")
            files_to_close.append(test)
            test_strings.append(test.read())

            try:
                result = open(os.path.join(absolute_path, result_file), "r")
                files_to_close.append(result)
                result_strings.append(result.read())
            except FileNotFoundError:
                msg = ("Result file not found for {}, did you mean to have a"
                       + "result file for {}?")
                print(msg.format(test_file, test_file))
                result_strings.append("")
    except Exception as e:
        print("Error Opening and Reading From Test Files!")
        raise(e)
    finally:
        for file in files_to_close:
            file.close()

    return zip(test_strings, result_strings)
