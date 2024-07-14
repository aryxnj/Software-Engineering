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


class TestPwd(unittest.TestCase):
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
    #     shutil.rmtree("dir1")

    def test_pwd_no_args(self):
        out = deque()
        path = os.getcwd()
        index_of_comp = path.index("comp")
        relative_path = path[index_of_comp:]
        eval("pwd", out)
        self.assertEqual(relative_path, "comp0010")

    def test_pwd_too_many_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("pwd test.txt", out)


if __name__ == "__main__":
    unittest.main()
