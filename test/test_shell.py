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


class TestShell(unittest.TestCase):
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

    def test_shell(self):
        out = deque()
        eval("echo foo", out)
        self.assertEqual(out.popleft(), "foo\n")
        self.assertEqual(len(out), 0)

    def test_semicolon(self):
        out = deque()
        eval("echo AAA; echo BBB", out)
        self.assertEqual(out.popleft(), "AAA\n")
        self.assertEqual(out.popleft(), "BBB\n")

    # def test_output_redirection_r(self):
    #     out = deque()
    #     eval("echo foo > test.txt", out)
    #     self.assertEqual(out.popleft(), "foo")
    #     # stdout = self.eval("cat test.txt", shell="/bin/bash")

    def test_output_redirection_l(self):
        out = deque()
        eval("echo foo < test.txt", out)
        self.assertEqual(out.popleft(), "foo test.txt\n")
        # stdout = self.eval("cat test.txt", shell="/bin/bash")


if __name__ == "__main__":
    unittest.main()
