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


class TestCut(unittest.TestCase):
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

    def test_cut_no_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("cut", out)

    def test_cut_two_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("cut -b test.txt", out)
        out = deque()

    def test_cut_three_no_b(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("cut 1 test.txt 2-3", out)
        out = deque()

    def test_cut_with_args_and_wrong_file(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("cut -b 1-3 no.txt", out)

    # def test_cut_with_args(self):
    #     out = deque()
    #     eval("cut -b 1-3", out)
    #     self.assertEqual(len(out), 0)

    def test_cut_with_args_and_file(self):
        out = deque()
        eval("cut -b 1-3 dir1/test.txt", out)
        self.assertEqual(out.popleft(), "ora\n")
        self.assertEqual(out.popleft(), "app\n")
        self.assertEqual(out.popleft(), "gra\n")
        self.assertEqual(out.popleft(), "ban\n")

    def test_cut_open_end(self):
        out = deque()
        eval("cut -b 2- dir1/test.txt", out)
        self.assertEqual(out.popleft(), "range\n")
        self.assertEqual(out.popleft(), "pple\n")
        self.assertEqual(out.popleft(), "rape\n")
        self.assertEqual(out.popleft(), "anana\n")

    def test_cut_one_char(self):
        out = deque()
        eval("cut -b 4 dir1/test.txt", out)
        self.assertEqual(out.popleft(), "n\n")
        self.assertEqual(out.popleft(), "l\n")
        self.assertEqual(out.popleft(), "p\n")
        self.assertEqual(out.popleft(), "a\n")

    def test_cut_out_range(self):
        out = deque()
        eval("cut -b 2-10 dir1/test.txt", out)
        self.assertEqual(out.popleft(), "range\n")
        self.assertEqual(out.popleft(), "pple\n")
        self.assertEqual(out.popleft(), "rape\n")
        self.assertEqual(out.popleft(), "anana\n")

    def test_cut_pipe(self):
        out = deque()
        eval("sort dir1/test.txt | cut -b 3", out)
        self.assertEqual(out.popleft(), "p\n")
        self.assertEqual(out.popleft(), "n\n")
        self.assertEqual(out.popleft(), "a\n")
        self.assertEqual(out.popleft(), "a\n")


if __name__ == "__main__":
    unittest.main()
