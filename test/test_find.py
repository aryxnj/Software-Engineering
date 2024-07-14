import unittest
import shutil


# current = sys.path
# new = current[0].replace("test", "src")
# sys.path.append(new)

from src.shell import eval
from collections import deque

# current = sys.path
# new = current[0].replace("src", "test")
# sys.path.append(new)
import os


class TestFind(unittest.TestCase):
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

    def test_find_no_args(self):
        out = deque()
        eval("find", out)
        self.assertEqual(len(out), 144)

    def test_find_missing_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("find dir1 -name", out)

    def test_find_wrong_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("find dir1 dir2 -name", out)

    def test_find_excess_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("find dir1 -name dir1 dir2", out)

    def test_find_with_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval(out, "./dir1/test.txt\n")

    def test_find_with_args_and_file(self):
        out = deque()
        eval("find -name test.txt", out)
        output_list = list(out)
        output_list.sort()
        output = ' '.join(output_list)
        self.assertEqual(output, "./dir1/test.txt\n")

    def test_find_with_args_and_file_asterisk(self):
        out = deque()
        eval("find -name *.txt", out)
        output_list = list(out)
        output_list.sort()
        output = ' '.join(output_list)
        self.assertEqual(output, "./dir1/example2.txt\n "
                                 "./dir1/example3.txt\n "
                                 "./dir1/test.txt\n "
                                 "./requirements.txt\n "
                                 "./temp.txt\n")

    def test_find_with_args_and_dir(self):
        out = deque()
        eval("find dir1 -name test.txt", out)
        self.assertEqual(out.popleft(), "dir1/dir1/test.txt\n")

    def test_find_with_args_and_dir_asterisk(self):
        out = deque()
        eval("find dir1 -name *.txt", out)
        output_list = list(out)
        output_list.sort()
        output = ' '.join(output_list)
        self.assertEqual(output, "dir1/example2.txt\n "
                                 "dir1/example3.txt\n "
                                 "dir1/test.txt\n")


if __name__ == "__main__":
    unittest.main()
