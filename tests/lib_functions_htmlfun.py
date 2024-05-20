import unittest
import sys

sys.path.append('../ecommquery')

from ecommquery.lib.functions.html import *


class TestHTMLfun(unittest.TestCase):
    def test_sanitize_html_div(self):
        input = "<div>Don't make me naked!</div>"
        expected = "Don't make me naked!"

        ret, stat = HTMLfun.sanitize(input)
        self.assertEqual(ret, expected)

    def test_sanitize_html_style_and_class(self):
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

    def test_sanitize_html_span(self):
        input      = "<p><span>Don't strip everything!</span></p>"
        expected = "<p>Don't strip everything!</p>"

        ret, stat = HTMLfun.sanitize(input)
        self.assertEqual(ret, expected)

    def test_sanitize_html_h1(self):
        input = ["<p><h1>Header</h1> and <h2>sub-header</h2> ... </p>",
                 "<h1>test</h1> ... <h4>test</h4>"]
        expected = ["<p><h2>Header</h2> and <h3>sub-header</h3> ... </p>",
                    "<h2>test</h2> ... <h3>test</h3>"]

        for idx, inp in enumerate(input):
            output, stat = HTMLfun.sanitize(inp, start_hlevel=2)
            self.assertEqual(expected[idx], output)

    def test_sanitize_html_empty(self):
        input = ["<p><u>part</u>ially<u>underline</u><b>text</b><b></b></p>"]
        expected = ["<p><u>part</u>ially<u>underline</u><b>text</b></p>"]

        for idx, inp in enumerate(input):
            output, stat = HTMLfun.sanitize(inp, start_hlevel=2)
            self.assertEqual(expected[idx], output)

    def test_sanitize_html_merge(self):
        input = ["<p><b>Bo</b><b>ld</b> and <u>Under</u><u>line</u></p>",
                 "<i>text</i> <i>.</i> and <i>text</i><i>.</i>",
                 "<p><b>B</b><u>U</u><b>O</b>   </p>",
                 "<p>1</p><p>1</p>"]
        expected = ["<p><b>Bold</b> and <u>Underline</u></p>",
                    "<i>text</i> <i>.</i> and <i>text.</i>",
                    "<p><b>B</b><u>U</u><b>O</b> </p>",
                    "<p>1</p><p>1</p>"]

        for idx, inp in enumerate(input):
            output, stat = HTMLfun.sanitize(inp, start_hlevel=2)
            self.assertEqual(expected[idx], output)

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


    def test_to_plain_text(self):
        input1 = "<p><h1>Header</h1> and <h2>sub-header</h2> ... </p>"
        expected1 = """Header
and
 sub-header
...
"""
        input2 = """Introduction.
        <p>Text <h1>Header</h1> and <h2>sub-header</h2> and   
        text here. </p>Ending 
        sentence."""
        expected2 = """Introduc
tion.
Text
Header
and
 sub-hea
der
and   
  
      
text 
here.
Ending 
 
       
sentence
."""
        input3 = """<p>12345678123456789</p>12345678"""
        expected3 = """12345678
12345678
9
12345678
"""

        out = HTMLfun.getPlainTextSuper(input1, max_colnums = 80)
        self.assertEqual(expected1, out)

        out = HTMLfun.getPlainTextSuper(input2, max_colnums = 8)
        self.assertEqual(expected2, out)

        out = HTMLfun.getPlainTextSuper(input3, max_colnums=8)
        self.assertEqual(expected3, out)

    def test_to_plain_text_file1(self):
        f_in = open("../tests/files/htmlfun_2-input.txt", 'r')
        f_exp = open("../tests/files/htmlfun_2-expected.txt", 'r')

        text = HTMLfun.getPlainTextSuper(f_in.read())
        print("BEGIN: \n" + text + "\nEND ---")

        self.assertEqual(text, f_exp.read())

        f_exp.close()
        f_in.close()

if __name__ == '__main__':
    unittest.main()
