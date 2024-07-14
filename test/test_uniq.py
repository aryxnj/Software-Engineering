import unittest
import tempfile
from hypothesis import given, strategies as st
from src.shell import eval
from collections import deque
import shutil
import os


class TestUniq(unittest.TestCase):
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
            f.write("aaa \n" "AAA \n" "bbb \n" "BBB \n" "CCC \n" "AAA \n")
        with open("dir1/example3.txt", "w") as f:
            f.write("")

    def tearDown(self):
        # Remove the directory and all its contents
        shutil.rmtree("dir1")

    def test_uniq_invalid_zero_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("uniq", out)

    def test_uniq_invalid_two_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("uniq -n dir1/example1.txt", out)

    def test_uniq_invalid_many_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("uniq -n -c dir1/example1.txt", out)

    def test_uniq_one_arg(self):
        out = deque()
        eval("uniq dir1/example2.txt", out)
        expected_output = [
            "aaa \n",
            "AAA \n",
            "bbb \n",
            "BBB \n",
            "CCC \n",
            "AAA \n",
        ]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    def test_uniq_two_args_i(self):
        out = deque()
        eval("uniq -i dir1/example2.txt", out)
        expected_output = [
            "aaa \n",
            "bbb \n",
            "CCC \n",
            "AAA \n",
        ]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    def test_uniq_two_args_redirection(self):
        out = deque()
        eval("uniq < dir1/example2.txt", out)
        expected_output = [
            "aaa \n",
            "AAA \n",
            "bbb \n",
            "BBB \n",
            "CCC \n",
            "AAA \n",
        ]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    # Here these 2
    def test_uniq_two_args_i_emptyfile(self):
        out = deque()
        eval("uniq -i dir1/example3.txt", out)
        self.assertEqual(out.popleft(), "\n")

    def test_uniq_one_arg_emptyfile(self):
        out = deque()
        eval("uniq dir1/example3.txt", out)
        self.assertEqual(out.popleft(), "\n")


class TestUniqProperties(unittest.TestCase):
    @given(
        st.sets(
            st.text(
                alphabet="".join([chr(i) for i in range(97, 123)]), min_size=1
            ),
            min_size=1,
        )
    )
    def test_uniq_exact_output(self, unique_lines):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            for line in unique_lines:
                tmp.write(line + "\n")
            tmp_path = tmp.name
        out = deque()
        eval(f"uniq {tmp_path}", out)
        output_lines = [line for line in out]
        expected_output = [line + "\n" for line in unique_lines] + ["\n"]
        self.assertEqual(output_lines, expected_output)
        os.remove(tmp_path)

    @given(
        st.sets(
            st.text(
                alphabet="".join([chr(i) for i in range(97, 123)]), min_size=1
            ),
            min_size=1,
        )
    )
    def test_uniq_all_unique_lines(self, unique_lines):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            for line in unique_lines:
                tmp.write(line + "\n")
            tmp_path = tmp.name
        out = deque()
        eval(f"uniq {tmp_path}", out)
        output_line_count = len(out)
        self.assertEqual(output_line_count, len(unique_lines) + 1)
        os.remove(tmp_path)

    """@given(st.lists(st.text(alphabet=''.join
    ([chr(i) for i in range(97, 123)]), min_size=1), unique=True, min_size=1))
    def test_uniq_case_insensitive(self, lines):
        # Create a list of lines with varying cases
        case_varied_lines = [line.lower() if i % 2 == 0
        else line.upper() for i, line in enumerate(lines)]

        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            for line in case_varied_lines:
                tmp.write(line + "\n")
            tmp_path = tmp.name

        out = deque()
        eval(f"uniq -i {tmp_path}", out)
        output_lines = list(out)

        # Convert all lines to lower case for comparison
        # also maintaining the newline characters
        unique_lines_lower = set(line.lower() for line in lines)
        expected_output = [line.lower + "\n" for line in unique_lines_lower]
        expected_output.sort()

        # Add the extra newline if uniq adds it at the end
        if output_lines[-1] == '\n':
            expected_output.append('\n')

        self.assertEqual(output_lines, expected_output)

        os.remove(tmp_path)"""


if __name__ == "__main__":
    unittest.main()
