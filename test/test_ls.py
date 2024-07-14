import unittest


# current = sys.path
# new = current[0].replace("test", "src")
# sys.path.append(new)

from src.shell import eval
from collections import deque
import shutil

# current = sys.path
# new = current[0].replace("src", "test")
# sys.path.append(new)
import os


class TestLs(unittest.TestCase):
    def setUp(self):
        os.makedirs("dir1", exist_ok=True)
        # Create files in the directory

        with open("dir1/test.txt", "w") as f:
            f.write("orange\napple\ngrape\nbanana\n")
        with open("dir1/example2.txt", "w") as f:
            f.write("Content of example2\n")
        with open("dir1/example3.txt", "w") as f:
            f.write("Content of example3")

    def tearDown(self):
        shutil.rmtree("dir1")

    def test_ls_no_args(self):
        print(os.getcwd())
        out = deque()
        eval("ls", out)
        self.assertEqual(len(out), 11)

    def test_ls_dir_count(self):
        # current = sys.path
        # index_comp0010 = current.index("comp0010")
        # new = current[:index_comp0010] + ["comp0010"]
        # sys.path.append(new)
        out = deque()
        eval("ls dir1", out)
        print(os.getcwd())
        self.assertEqual(len(out), 3)

    def test_ls_dir_file(self):
        # current = sys.path
        # index_comp0010 = current.index("comp0010")
        # new = current[:index_comp0010] + ["comp0010"]
        # sys.path.append(new)
        out = deque()
        eval("ls dir1", out)
        print(os.getcwd())
        output_list = list(out)
        output_list.sort()  # Sort the list
        output = ' '.join(output_list)  # Join the sorted list into a string
        self.assertEqual(
            output, "example2.txt\n example3.txt\n test.txt\n"
        )

    def test_ls_wrong_dir(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("ls system_test system_test", out)

    def test_ls_invalid_dir(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("ls syste", out)


if __name__ == "__main__":
    unittest.main()
