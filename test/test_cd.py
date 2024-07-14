import unittest


# current = sys.path
# new = current[0].replace("test", "src")
# sys.path.append(new)

from src.shell import eval
from collections import deque

# current = sys.path
# new = current[0].replace("src", "test")
# sys.path.append(new)
import os


class TestCd(unittest.TestCase):
    def setUp(self):
        os.makedirs("dir1", exist_ok=True)
        # Create files in the directory

        with open("dir1/test.txt", "w") as f:
            f.write("orange\napple\ngrape\nbanana\n")
        with open("dir1/example2.txt", "w") as f:
            f.write("Content of example2\n")
        with open("dir1/example3.txt", "w") as f:
            f.write("Content of example3")

    # def tearDown(self):
    #     # Remove the directory and all its contents
    #     shutil.rmtree("dir1"))

    def test_cd_no_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("cd", out)

    def test_cd_dir(self):
        path = os.getcwd()
        index_of_comp = path.index("comp")
        out = deque()
        eval("cd src", out)
        new_path = os.getcwd()
        index_of_comp = new_path.index("comp")
        new_relative_path = new_path[index_of_comp:]
        self.assertEqual(new_relative_path, "comp0010/src")

    '''def test_cd_dir_and_out(self):
        out = deque()
        path = os.getcwd()
        index_of_comp = path.index("comp")
        relative_path = path[index_of_comp:]
        out = deque()
        eval("cd src", out)
        eval("cd ..", out)
        self.assertEqual(relative_path, "comp0010")'''

    def test_cd_invalid_dir(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("cd no", out)

    def test_cd_pw_protected(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("cd pw_protected_file.zip", out)

    def test_cd_parent(self):
        out = deque()
        eval("cd ..", out)
        path = os.getcwd()
        index_of_comp = path.index("comp")
        relative_path = path[index_of_comp:]
        self.assertEqual(relative_path, "comp0010")

    def test_cd_too_many_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("cd src src", out)


if __name__ == "__main__":
    unittest.main()
