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


class TestSed(unittest.TestCase):
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

    def test_sed_no_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("sed", out)

    def test_sed_wrong_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("sed 's/a/x/' ", out)

    def test_sed_wrong_file(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("sed 's/a/x/' rand.txt", out)

    def test_sed_wrong_pattern(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("sed s/a/x/ dir1/test.txt", out)

    def test_sed_wrong_pattern_2(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("sed 'g/a/x/' dir1/test.txt", out)

    def test_sed_no_flag(self):
        out = deque()
        eval("sed 's/a/x/' dir1/test.txt", out)
        self.assertEqual(out.popleft(), "orxnge\n")
        self.assertEqual(out.popleft(), "xpple\n")
        self.assertEqual(out.popleft(), "grxpe\n")
        self.assertEqual(out.popleft(), "bxnana\n")

    def test_sed_g_flag(self):
        out = deque()
        eval("sed 's/a/x/g' dir1/test.txt", out)
        self.assertEqual(out.popleft(), "orxnge\n")
        self.assertEqual(out.popleft(), "xpple\n")
        self.assertEqual(out.popleft(), "grxpe\n")
        self.assertEqual(out.popleft(), "bxnxnx\n")

    def test_sed_wrong_flag(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("sed 's/a/x/y' dir1/test.txt", out)


if __name__ == "__main__":
    unittest.main()
