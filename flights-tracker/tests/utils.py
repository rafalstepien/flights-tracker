from pathlib import Path


def get_test_file_path(filename):
    conftest_path = Path(__file__).resolve().parent
    tests_data_path = conftest_path / "data/"
    return str(tests_data_path / filename)


def read_test_file(filename):
    file_path = get_test_file_path(filename)
    with open(file_path, "r") as f:
        content = f.read()
    return content
