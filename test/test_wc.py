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


class TestWc(unittest.TestCase):
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

    def test_wc_no_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc", out)

    def test_wc_wrong_file(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc tes.txt", out)

    def test_wc_one_arg(self):
        out = deque()
        eval("wc dir1/test.txt", out)
        self.assertEqual(out.popleft(), "4\n")
        self.assertEqual(out.popleft(), "4\n")
        self.assertEqual(out.popleft(), "26\n")

    def test_wc_l(self):
        out = deque()
        eval("wc -l dir1/test.txt", out)
        self.assertEqual(out.popleft(), "4\n")

    def test_wc_w(self):
        out = deque()
        eval("wc -w dir1/test.txt", out)
        self.assertEqual(out.popleft(), "4\n")

    def test_wc_c(self):
        out = deque()
        eval("wc -c dir1/test.txt", out)
        self.assertEqual(out.popleft(), "26\n")

    def test_wc_m(self):
        out = deque()
        eval("wc -m dir1/test.txt", out)
        self.assertEqual(out.popleft(), "26\n")

    def test_wc_l_wrong_file(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc -l dir1/test2.txt", out)

    def test_wc_w_wrong_file(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc -w dir1/test2.txt", out)

    def test_wc_c_wrong_file(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc -c dir1/test2.txt", out)

    def test_wc_m_wrong_file(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc -m dir1/test2.txt", out)

    def test_wc_two_wrong_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc -x dir1/test.txt", out)

    def test_wc_four_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc -l dir1/test.txt dir1/example2 -c", out)

    def test_wc_three_l(self):
        out = deque()
        eval("wc -l dir1/test.txt dir1/example2.txt", out)
        self.assertEqual(out.popleft(), "5\n")

    def test_wc_three_w(self):
        out = deque()
        eval("wc -w dir1/test.txt dir1/example2.txt", out)
        self.assertEqual(out.popleft(), "7\n")

    def test_wc_three_c(self):
        out = deque()
        eval("wc -c dir1/test.txt dir1/example2.txt", out)
        self.assertEqual(out.popleft(), "46\n")

    def test_wc_three_m(self):
        out = deque()
        eval("wc -m dir1/test.txt dir1/example2.txt", out)
        self.assertEqual(out.popleft(), "46\n")

    def test_wc_l_wrong_file1(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc -l dir1/test2.txt dir1/example2.txt", out)

    def test_wc_w_wrong_file1(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc -w dir1/test2.txt dir1/example2.txt", out)

    def test_wc_c_wrong_file1(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc -c dir1/test2.txt dir1/example2.txt", out)

    def test_wc_m_wrong_file1(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc -m dir1/test2.txt dir1/example2.txt", out)

    def test_wc_l_wrong_file2(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc -l dir1/test2.txt dir1/example2.txt", out)

    def test_wc_w_wrong_file2(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc -w dir1/test2.txt dir1/example2.txt", out)

    def test_wc_c_wrong_file2(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc -c dir1/test2.txt dir1/example2.txt", out)

    def test_wc_m_wrong_file2(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("wc -m dir1/test2.txt dir1/example2.txt", out)


if __name__ == "__main__":
    unittest.main()
