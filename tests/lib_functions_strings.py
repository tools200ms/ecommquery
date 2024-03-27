import unittest
import sys

sys.path.append('../ecommquery')

from ecommquery.lib.functions.strings import *


class TestStrings(unittest.TestCase):
    def test_sanitize_html_1(self):
        input = "<div>Don't make me naked!</div>"
        expected = "Don't make me naked!"

        self.assertEqual(StringOp.sanitize_html(input), expected)

    def test_sanitize_html_2(self):
        input      = "<p class=\"keepme\"><b style=\"color: red\">I</b> will <i>survive</i></p>"
        expected1 = "<p class=\"keepme\"><b style=\"color: red\">I</b> will <i>survive</i></p>"
        expected2 = "<p><b style=\"color: red\">I</b> will <i>survive</i></p>"
        expected3 = "<p><b>I</b> will <i>survive</i></p>"

        self.assertEqual(StringOp.sanitize_html(input), expected1)
        self.assertEqual(StringOp.sanitize_html(input, True), expected2)
        self.assertEqual(StringOp.sanitize_html(input, True, True), expected3)

    def test_sanitize_html_3(self):
        input      = "<p><span>Don't strip everything!</span></p>"
        expected = "<p>Don't strip everything!</p>"

        self.assertEqual(StringOp.sanitize_html(input), expected)

    def test_sanitize_html_file1(self):
        f_in = open("../tests/files/stringop_test1-input.txt", 'r')
        #f_exp = open("../tests/files/stringop_test1-expected.txt", 'r')

        print( StringOp.trim_tags( StringOp.sanitize_html( f_in.read() ), [] ) )
        #print(StringOp.trim_tags(f_exp.read(), []))
        #self.assertEqual(StringOp.sanitize_html(f_in.read()), f_exp.read())

        #f_exp.close()
        f_in.close()

if __name__ == '__main__':
    unittest.main()
