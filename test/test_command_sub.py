import unittest

from src.shell import eval
from collections import deque
import shutil
import os


class TestPipe(unittest.TestCase):
    def setUp(self):
        os.makedirs("dir1", exist_ok=True)
        # Create files in the directory
        with open("dir1/example1.txt", "w") as f:
            f.write(
                "This is line 1 \n"
                "This is line 2 \n"
                "This is line 3 \n"
                "This is line 4 \n"
                "This is line 5 \n"
                "This is line 6 \n"
                "This is line 7 \n"
                "This is line 8 \n"
                "This is line 9 \n"
                "This is the 10th \n"
                "This is line 11 \n"
                "This is the last line \n"
            )
        with open("dir1/example2.txt", "w") as f:
            f.write("aaa \n" "AAA 1 \n" "bbb \n" "BBB \n" "CCC \n" "AAA 2 \n")
        with open("dir1/example3.txt", "w") as f:
            f.write("")
        with open("dir1/example4.txt", "w") as f:
            f.write("line")

    def tearDown(self):
        # Remove the directory and all its contents
        shutil.rmtree("dir1")

    def test_cat_redirection(self):
        out = deque()
        eval("cat < dir1/example1.txt", out)
        expected_output = [
            "This is line 1 \n"
            "This is line 2 \n"
            "This is line 3 \n"
            "This is line 4 \n"
            "This is line 5 \n"
            "This is line 6 \n"
            "This is line 7 \n"
            "This is line 8 \n"
            "This is line 9 \n"
            "This is the 10th \n"
            "This is line 11 \n"
            "This is the last line \n"
        ]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    def test_cat_redirection_with_pipe(self):
        out = deque()
        eval("cat < dir1/example1.txt | grep line", out)
        expected_output = [
            "This is line 1 \n"
            "This is line 2 \n"
            "This is line 3 \n"
            "This is line 4 \n"
            "This is line 5 \n"
            "This is line 6 \n"
            "This is line 7 \n"
            "This is line 8 \n"
            "This is line 9 \n"
            "This is the 10th \n"
            "This is line 11 \n"
            "This is the last line \n"
        ]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    def test_echo_command_sub(self):
        out = deque()
        eval("echo `echo foo`", out)
        self.assertEqual(out.popleft(), "foo\n")
        self.assertEqual(len(out), 0)

    def test_command_sub_sort_find(self):
        out = deque()
        eval("cat `find -name example1.txt` | sort", out)
        expected_output = [
            "This is line 1 \n",
            "This is line 11 \n",
            "This is line 2 \n",
            "This is line 3 \n",
            "This is line 4 \n",
            "This is line 5 \n",
            "This is line 6 \n",
            "This is line 7 \n",
            "This is line 8 \n",
            "This is line 9 \n",
            "This is the 10th \n",
            "This is the last line \n",
        ]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    def test_echo_output_redirection(self):
        out = deque()
        eval("echo foo > dir1/example3.txt", out)
        expected_output = ["foo"]
        with open("dir1/example3.txt", "r") as f:
            for line in f:
                self.assertEqual(line, expected_output.pop(0))

    def test_echo_output_redirection_double(self):
        out = deque()
        eval("echo foo >> dir1/example3.txt", out)
        expected_output = ["foo"]
        with open("dir1/example3.txt", "r") as f:
            for line in f:
                self.assertEqual(line, expected_output.pop(0))

    def test_command_sub_sort_find_indbquotes(self):
        out = deque()
        eval("\"cat `find -name example1.txt` | sort\"", out)
        expected_output = [
            "This is line 1 \n",
            "This is line 11 \n",
            "This is line 2 \n",
            "This is line 3 \n",
            "This is line 4 \n",
            "This is line 5 \n",
            "This is line 6 \n",
            "This is line 7 \n",
            "This is line 8 \n",
            "This is line 9 \n",
            "This is the 10th \n",
            "This is the last line \n",
        ]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    def test_echo_command_sub_indbquotes1(self):
        out = deque()
        eval("\"echo `echo foo`\"", out)
        self.assertEqual(out.popleft(), "foo\n")
        self.assertEqual(len(out), 0)

    def test_echo_command_sub_indbquotes2(self):
        out = deque()
        eval("echo a\"b\"c", out)
        self.assertEqual(out.popleft(), "abc\n")
        self.assertEqual(len(out), 0)

    def test_echo_command_sub_insquotes(self):
        out = deque()
        eval("echo ab\'c\'", out)
        self.assertEqual(out.popleft(), "abc\n")
        self.assertEqual(len(out), 0)

    def test_echo_command_sub_empty_quotes(self):
        out = deque()
        eval("echo a\"\"", out)
        self.assertEqual(out.popleft(), "a \n")
        self.assertEqual(len(out), 0)

    def test_double_echo_command_sub(self):
        out = deque()
        eval("echo \"a`echo abc`c\"", out)
        self.assertEqual(out.popleft(), "aabcc\n")
        self.assertEqual(len(out), 0)


if __name__ == "__main__":
    unittest.main()
