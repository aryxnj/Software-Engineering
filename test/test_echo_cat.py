import unittest
from hypothesis import given, strategies as st
from src.shell import eval
from collections import deque
import shutil
import os


class TestEchoCat(unittest.TestCase):
    def setUp(self):
        os.makedirs("dir1", exist_ok=True)
        # Create files in the directory
        with open("dir1/example1.txt", "w") as f:
            f.write("Hello World!")
        with open("dir1/example2.txt", "w") as f:
            f.write("Content of example2")
        with open("dir1/example3.txt", "w") as f:
            f.write("Content of example3")

    def tearDown(self):
        # Remove the directory and all its contents
        shutil.rmtree("dir1")

    def test_shell(self):
        out = deque()
        eval("echo foo", out)
        self.assertEqual(out.popleft(), "foo\n")
        self.assertEqual(len(out), 0)

    def test_echo_no_args(self):
        out = deque()
        eval("echo", out)
        self.assertEqual(out.popleft(), "\n")
        self.assertEqual(len(out), 0)

    def test_echo_one_arg(self):
        out = deque()
        eval("echo foo", out)
        self.assertEqual(out.popleft(), "foo\n")
        self.assertEqual(len(out), 0)

    def test_echo_globbed(self):
        out = deque()
        eval("echo dir1/*.txt", out)
        output_list = list(out)
        output_list.sort()
        output = ' '.join(output_list)
        self.assertEqual(
            output, "dir1/example1.txt dir1/example3.txt dir1/example2.txt\n"
        )

    def test_echo_no_globbed(self):
        out = deque()
        eval("echo *.foo", out)
        self.assertEqual(out.popleft(), "*.foo\n")

    def test_cat_no_redirection(self):
        out = deque()
        eval("cat dir1/example1.txt", out)
        self.assertEqual(out.popleft(), "Hello World!\n")

    def test_cat_with_redirection(self):
        out = deque()
        eval("cat < dir1/example1.txt", out)
        self.assertEqual(out.popleft(), "Hello World!\n")

    # def test_cat_no_args(self):
    #     out = deque()
    #     with self.assertRaises(IndexError):
    #         eval("cat", out)
    #     # self.assertEqual(out.popleft(), "\n")

    def test_cat_multiple_args(self):
        out = deque()
        eval("cat dir1/example1.txt dir1/example2.txt", out)
        self.assertEqual(out.popleft(), "Hello World!\n")
        self.assertEqual(out.popleft(), "Content of example2\n")


class TestPropertyEchoCat(unittest.TestCase):
    """
    @given(
        st.text(
            alphabet="".join(
                [chr(i) for i in range(48, 58)]
                + [chr(i) for i in range(65, 91)]  # Numbers 0-9
                + [chr(i) for i in range(97, 123)]  # Uppercase A-Z
            )
        )
    )  # Lowercase a-z
    def test_echo(self, s):
        out = deque()
        eval(f"echo {s}", out)
        self.assertEqual(out.popleft(), f"{s}\n")
    """

    @given(st.just(""))
    def test_echo_empty_string(self, s):
        out = deque()
        eval("echo", out)
        self.assertEqual(out.popleft(), "\n")


"""
    @given(
        st.text(
            alphabet="".join(
                [chr(i) for i in range(65, 91)]  # Numbers 0-9
                + [chr(i) for i in range(97, 123)]  # Uppercase A-Z
            )
        )
    )
    def test_cat_single_file(self, content):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        out = deque()
        eval(f"cat {tmp_path}", out)
        self.assertEqual(out.popleft(), "\n")
        self.assertEqual(out.popleft(), content)
        os.remove(tmp_path)
"""

"""
        @given(st.lists(st.text(alphabet=''.join(
        [chr(i) for i in range(65, 91)] +  # Uppercase A-Z
        [chr(i) for i in range(97, 123)]  # Lowercase a-z
    )), min_size=1))
    def test_cat_multiple_files(self, contents):
        paths = []
        try:
            for content in contents:
                with tempfile.NamedTemporaryFile
                    (mode='w+', delete=False) as tmp:
                    tmp.write(content)
                    paths.append(tmp.name)
            out = deque()
            eval(f"cat {' '.join(paths)}", out)
            self.assertEqual(out.popleft(), ''.join(contents))
        finally:
            for path in paths:
                os.remove(path)
"""


if __name__ == "__main__":
    unittest.main()
