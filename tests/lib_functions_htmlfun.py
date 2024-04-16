import unittest
import sys

sys.path.append('../ecommquery')

from ecommquery.lib.functions.html import *


class TestHTMLfun(unittest.TestCase):
    def test_sanitize_html_1(self):
        input = "<div>Don't make me naked!</div>"
        expected = "Don't make me naked!"

        ret, stat = HTMLfun.sanitize(input)
        self.assertEqual(ret, expected)

    def test_sanitize_html_2(self):
        input      = "<p class=\"keepme\"><b style=\"color: red\">I</b> will <i>survive</i></p>"
        expected1 = "<p class=\"keepme\"><b style=\"color: red\">I</b> will <i>survive</i></p>"
        expected2 = "<p><b style=\"color: red\">I</b> will <i>survive</i></p>"
        expected3 = "<p><b>I</b> will <i>survive</i></p>"

        ret, stat = HTMLfun.sanitize(input)
        self.assertEqual(ret, expected1)

        ret, stat = HTMLfun.sanitize(input, True)
        self.assertEqual(ret, expected2)

        ret, stat = HTMLfun.sanitize(input, True, True)
        self.assertEqual(ret, expected3)

    def test_sanitize_html_3(self):
        input      = "<p><span>Don't strip everything!</span></p>"
        expected = "<p>Don't strip everything!</p>"

        ret, stat = HTMLfun.sanitize(input)
        self.assertEqual(ret, expected)

    def test_sanitize_html_file1(self):
        f_in = open("../tests/files/htmlfun_1-input.txt", 'r')
        f_exp = open("../tests/files/htmlfun_1-expected.txt", 'r')

        res, stat = HTMLfun.sanitize(f_in.read())
        self.assertEqual(res, f_exp.read())

        f_exp.close()
        f_in.close()

    def test_cut_head1(self):
        input1 = "<p></p><p><b>Head</b></p><p>Text</p><p><b>TAIL to KEEP</b></p>"
        expected1 = "<p>Text</p><p><b>TAIL to KEEP</b></p>"

        input2 = "<p></p><p>Header</p><p>Header</p><p></p><p>Header</p>"
        expected2 = "<p>Header</p><p></p><p>Header</p>"

        input3 = "<p></p><p><i>Header</i></p><p><i>Header</i></p><p></p><p>Body</p>"
        input3b = "<p></p><p><i>Hea</i><i>der</i></p><p><i>Header</i></p><p></p><p>Body</p>"
        expected31 = "<p><i>Header</i></p><p><i>Header</i></p><p></p><p>Body</p>"

        expected32 = "<p><i>Header</i></p><p></p><p>Body</p>"

        res, stat = HTMLfun.cut_head(input1, ['b'])
        self.assertEqual(expected1, res)

        res, stat = HTMLfun.cut_head(input2, text_pattern = 'Header')
        self.assertEqual(expected2, res)

        res, stat = HTMLfun.cut_head(input3, text_pattern='Header')
        self.assertEqual(expected31, res)

        res, stat = HTMLfun.cut_head(input3, ['i'], 'Header')
        self.assertEqual(expected32, res)

        #res, stat = HTMLfun.cut_head(input3b, ['i'], 'Header')
        #self.assertEqual(expected32, res)

    def test_cut_h1(self):
        input = "<p><h1>Header</h1> and <h2>sub-header</h2> ... </p>"
        expected = "<p><h2>Header</h2> and <h3>sub-header</h3> ... </p>"

        ret, stat = HTMLfun.sanitize(input, start_hlevel = 2)
        self.assertEqual(expected, ret)

if __name__ == '__main__':
    unittest.main()
