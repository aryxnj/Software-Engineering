import unittest
from hypothesis import given, strategies as st
import tempfile
from src.shell import eval
from collections import deque
import shutil
import os


class TestGrep(unittest.TestCase):
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
            f.write(
                "AAA 1 \n"
                "AAA 2 \n"
                "AAA 3 \n"
                "AAA 4 \n"
                "AAA 5 \n"
                "AAA 6 \n"
            )
        with open("dir1/example3.txt", "w") as f:
            f.write("AAA Content of example3")

    def tearDown(self):
        # Remove the directory and all its contents
        shutil.rmtree("dir1")

    def test_grep_normal(self):
        out = deque()
        eval("grep AAA dir1/example2.txt", out)
        expected_output = [
            "AAA 1 \n",
            "AAA 2 \n",
            "AAA 3 \n",
            "AAA 4 \n",
            "AAA 5 \n",
            "AAA 6 \n",
        ]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    def test_grep_multiple_files(self):
        out = deque()
        eval("grep AAA dir1/example2.txt dir1/example3.txt", out)
        expected_output = [
            "dir1/example2.txt:AAA 1 \n",
            "dir1/example2.txt:AAA 2 \n",
            "dir1/example2.txt:AAA 3 \n",
            "dir1/example2.txt:AAA 4 \n",
            "dir1/example2.txt:AAA 5 \n",
            "dir1/example2.txt:AAA 6 \n",
            "dir1/example3.txt:AAA Content of example3",
        ]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    def test_grep_zero_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("grep", out)

    def test_grep_one_arg(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("grep AAA", out)

    def test_grep_invalid_file(self):
        out = deque()
        with self.assertRaises(FileNotFoundError):
            eval("grep AAA dir1/example4.txt", out)


class TestPropertyGrep(unittest.TestCase):
    @given(
        st.lists(
            st.text(
                alphabet="".join([chr(i) for i in range(97, 123)]), min_size=1
            ),
            min_size=1,
        ),
        st.text(
            min_size=1, alphabet="".join([chr(i) for i in range(97, 123)])
        ),
    )
    def test_grep_line_count(self, file_lines, pattern):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            for line in file_lines:
                tmp.write(line + "\n")
            tmp_path = tmp.name

        out = deque()
        eval(f"grep {pattern} {tmp_path}", out)
        grep_output_count = len(out)

        self.assertLessEqual(grep_output_count, len(file_lines))

        os.remove(tmp_path)

    @given(
        st.text(
            min_size=1,
            max_size=10,
            alphabet="".join([chr(i) for i in range(97, 123)]),
        ),
        st.integers(min_value=5000, max_value=10000),
    )  # 5k to 10k lines
    def test_grep_large_file(self, pattern, num_lines):
        large_content = "\n".join([pattern] * num_lines)
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            tmp.write(large_content)
            tmp_path = tmp.name

        out = deque()
        eval(f"grep {pattern} {tmp_path}", out)
        grep_output_count = len(out)

        self.assertEqual(grep_output_count, num_lines)

        os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
