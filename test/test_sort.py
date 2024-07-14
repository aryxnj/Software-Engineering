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


class TestSort(unittest.TestCase):
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

    def test_sort_no_args(self):
        out = deque()
        eval("sort", out)
        self.assertEqual(len(out), 0)

    def test_sort_wrong_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("sort -r", out)

    def test_sort_excess_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("sort test.txt -r test.txt", out)

    def test_sort_and_file(self):
        out = deque()
        eval("sort -r dir1/test.txt", out)
        self.assertEqual(out.popleft(), "orange\n")
        self.assertEqual(out.popleft(), "grape\n")
        self.assertEqual(out.popleft(), "banana\n")
        self.assertEqual(out.popleft(), "apple\n")

    def test_sort_stdin_file(self):
        out = deque()
        eval("sort < dir1/test.txt", out)
        self.assertEqual(out.popleft(), "apple\n")
        self.assertEqual(out.popleft(), "banana\n")
        self.assertEqual(out.popleft(), "grape\n")
        self.assertEqual(out.popleft(), "orange\n")

    def test_sort_arg(self):
        out = deque()
        eval("sort dir1/test.txt", out)
        self.assertEqual(out.popleft(), "apple\n")
        self.assertEqual(out.popleft(), "banana\n")
        self.assertEqual(out.popleft(), "grape\n")
        self.assertEqual(out.popleft(), "orange\n")

    def test_pipe_sort(self):
        out = deque()
        cmdline = "cat dir1/test.txt dir1/example2.txt | sort"
        eval(cmdline, out)
        self.assertEqual(out.popleft(), "Content of example2\n")
        self.assertEqual(out.popleft(), "apple\n")
        self.assertEqual(out.popleft(), "banana\n")
        self.assertEqual(out.popleft(), "grape\n")
        self.assertEqual(out.popleft(), "orange\n")

    # def test_pipe_sort_r(self):
    #     out = deque()
    #     cmdline = "cat dir1/test.txt dir1/example2.txt | sort -r"
    #     eval(cmdline, out)
    #     self.assertEqual(out.popleft(), "orange\n")
    #     self.assertEqual(out.popleft(), "grape\n")
    #     self.assertEqual(out.popleft(), "Content of example2\n")
    #     self.assertEqual(out.popleft(), "banana\n")
    #     self.assertEqual(out.popleft(), "apple\n")

    # def test_pipe_sort_l(self):
    #     out = deque()
    #     cmdline = "cat dir1/test.txt dir1/example2.txt | sort <"
    #     eval(cmdline, out)
    #     self.assertEqual(out.popleft(), "apple\n")
    #     self.assertEqual(out.popleft(), "banana\n")
    #     self.assertEqual(out.popleft(), "Content of example2\n")
    #     self.assertEqual(out.popleft(), "grape\n")
    #     self.assertEqual(out.popleft(), "orange\n")


if __name__ == "__main__":
    unittest.main()
