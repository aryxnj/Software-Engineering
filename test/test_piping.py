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

    def tearDown(self):
        # Remove the directory and all its contents
        shutil.rmtree("dir1")

    def test_pipe_cat_grep(self):
        out = deque()
        eval("cat dir1/example2.txt | grep AAA", out)
        expected_output = ["AAA 1 \n", "AAA 2 \n"]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    def test_pipe_cat_uniq(self):
        out = deque()
        eval("cat dir1/example2.txt | uniq", out)
        expected_output = [
            "aaa \n",
            "AAA 1 \n",
            "bbb \n",
            "BBB \n",
            "CCC \n",
            "AAA 2 \n",
        ]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    def test_pipe_cat_uniq_i(self):
        out = deque()
        eval("cat dir1/example2.txt | uniq -i", out)
        expected_output = [
            "aaa \n",
            "AAA 1 \n",
            "bbb \n",
            "CCC \n",
            "AAA 2 \n",
        ]
        print(out)
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    def test_pipe_cat_uniq_i_empty_file(self):
        out = deque()
        eval("cat dir1/example3.txt | uniq -i", out)
        self.assertEqual(out.popleft(), "\n")

    def test_pipe_cat_uniq_i_invalid_file(self):
        out = deque()
        with self.assertRaises(FileNotFoundError):
            eval("cat dir1/example4.txt | uniq -i", out)

    def test_pipe_cat_uniq_empty_file(self):
        out = deque()
        eval("cat dir1/example3.txt | uniq", out)
        self.assertEqual(out.popleft(), "\n")

    def test_pipe_echo_cat(self):
        out = deque()
        eval("echo abc | cat", out)
        self.assertEqual(out.popleft(), "abc\n")

    def test_pipe_cat_head(self):
        out = deque()
        eval("cat dir1/example1.txt | head -n 5", out)
        expected_output = [
            "This is line 1 \n",
            "This is line 2 \n",
            "This is line 3 \n",
            "This is line 4 \n",
            "This is line 5 \n",
        ]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    def test_pipe_cat_tail(self):
        out = deque()
        eval("cat dir1/example1.txt | tail -n 5", out)
        expected_output = [
            "This is line 8 \n",
            "This is line 9 \n",
            "This is the 10th \n",
            "This is line 11 \n",
            "This is the last line \n",
        ]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)


if __name__ == "__main__":
    unittest.main()
