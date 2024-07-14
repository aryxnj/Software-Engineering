import unittest
import hashlib
import tempfile
from hypothesis import given, strategies as st
from src.shell import eval
from collections import deque
import shutil
import os


class TestTail(unittest.TestCase):
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
                "This is line 10 \n"
                "This is line 11 \n"
                "This is the last line \n"
            )
        with open("dir1/example2.txt", "w") as f:
            f.write("Content of example2")
        with open("dir1/example3.txt", "w") as f:
            f.write("Content of example3")

    def tearDown(self):
        # Remove the directory and all its contents
        shutil.rmtree("dir1")

    def test_tail_zero_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("tail", out)

    def test_tail_one_arg(self):
        out = deque()
        eval("tail dir1/example1.txt", out)
        expected_output = [
            "This is line 3 \n",
            "This is line 4 \n",
            "This is line 5 \n",
            "This is line 6 \n",
            "This is line 7 \n",
            "This is line 8 \n",
            "This is line 9 \n",
            "This is line 10 \n",
            "This is line 11 \n",
            "This is the last line \n",
        ]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    def test_tail_two_args(self):
        out = deque()
        eval("tail -n dir1/example1.txt", out)
        expected_output = [
            "This is line 3 \n",
            "This is line 4 \n",
            "This is line 5 \n",
            "This is line 6 \n",
            "This is line 7 \n",
            "This is line 8 \n",
            "This is line 9 \n",
            "This is line 10 \n",
            "This is line 11 \n",
            "This is the last line \n",
        ]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    def test_tail_three_args(self):
        out = deque()
        eval("tail -n 3 dir1/example1.txt", out)
        expected_output = [
            "This is line 10 \n",
            "This is line 11 \n",
            "This is the last line \n",
        ]
        for line in expected_output:
            self.assertEqual(out.popleft(), line)

    def test_tail_wrong_three_args(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("tail -f 5 dir1/example1.txt", out)

    def test_tail_lines_not_int(self):
        out = deque()
        with self.assertRaises(Exception):
            eval("tail -n a dir1/example1.txt", out)

    def test_tail_no_file(self):
        out = deque()
        with self.assertRaises(FileNotFoundError):
            eval("tail -n 3 dir1/example4.txt", out)


class TestTailProperty(unittest.TestCase):
    # Computing checksum of a file, to compare before and after tail
    def compute_checksum(self, file_path):
        hasher = hashlib.sha256()
        with open(file_path, "rb") as file:
            buf = file.read()
            hasher.update(buf)
        return hasher.hexdigest()

    # Checking that tail does not alter the file
    @given(
        st.text(alphabet=st.characters(blacklist_characters="\n"), min_size=1)
    )
    def test_tail_does_not_alter_file(self, content):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        checksum_before = self.compute_checksum(tmp_path)
        out = deque()
        eval(f"tail {tmp_path}", out)  # Change to 'tail'
        checksum_after = self.compute_checksum(tmp_path)
        self.assertEqual(checksum_before, checksum_after)
        os.remove(tmp_path)

    # Checking that tail is invariant to file extension:
    # .txt and .md files with the same content should have the same output
    @given(
        st.text(alphabet="".join([chr(i) for i in range(32, 127)]), min_size=1)
    )
    def test_tail_invariance_to_extension(self, content):
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".txt", delete=False
        ) as txt_file, tempfile.NamedTemporaryFile(
            mode="w+", suffix=".md", delete=False
        ) as md_file:
            txt_file.write(content)
            txt_file_path = txt_file.name
            md_file.write(content)
            md_file_path = md_file.name
        out_txt = deque()
        eval(f"tail {txt_file_path}", out_txt)  # Change to 'tail'
        out_md = deque()
        eval(f"tail {md_file_path}", out_md)  # Change to 'tail'
        self.assertEqual(list(out_txt), list(out_md))
        os.remove(txt_file_path)
        os.remove(md_file_path)


if __name__ == "__main__":
    unittest.main()
