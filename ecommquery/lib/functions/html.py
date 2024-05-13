from bs4 import BeautifulSoup, NavigableString, Tag

from ecommquery.exceptions import CallError
from ecommquery.lib.atomic.description import HTMLDescription


# String operations:
class HTMLfun:
    __header_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    __format_tags = ['p', 'br']
    __style_tags = ['b', 'i', 'strong', 'em', 'u']
    __table_tags = ['table', 'tbody', 'th', 'tr', 'td']
    __list_tags = ['ul', 'ol', 'li']

    @staticmethod
    def mapToPlainText(html: str = None, max_colnum = 80, parent_tag = None, contents = None, line = 0, column = 0):
        if html != None:
            soup = BeautifulSoup(html, 'html.parser')
            contents = soup.contents

        text = ''

        for el in contents:
            if isinstance(el, NavigableString):
                el_idx = contents.index(el)
                if parent_tag != None and (line + column) != 0 and el_idx == 0:
                    text += HTMLfun._opentag_to_plain(parent_tag.name)
                elif isinstance(contents[el_idx - 1], Tag):
                    text += HTMLfun._closetag_to_plain(contents[el_idx - 1].name)

                text += el.strip()
                column += len(text)
            elif isinstance(el, Tag):
                text += HTMLfun.mapToPlainText(parent_tag = el, contents = el.contents, line = line, column = column)
            # ignore other element types (e.g. comments)

        return text

    @staticmethod
    def _opentag_to_plain(tag_name: str):
        if tag_name in HTMLfun.__header_tags:
            h_idx = HTMLfun.__header_tags.index(tag_name)
            return '\n' + (' ' * h_idx)

        if tag_name in HTMLfun.__format_tags:
            return '\n\n'

        if tag_name in HTMLfun.__style_tags:
            return ' '

        if tag_name in HTMLfun.__table_tags:
            return {'table': '\n\n', 'tbody': '',
                    'th': '\n', 'tr': '\n',
                    'td': '    '}[tag_name]

        if tag_name in HTMLfun.__list_tags:
            return {'ul': '\n', 'ol': '\n',
                    'li': ' * '}[tag_name]

        raise CallError('Unspecified tag, was HTML sanitize before calling this function?')

    @staticmethod
    def _closetag_to_plain(tag_name: str):
        if tag_name in HTMLfun.__header_tags:
            return '\n'

        if tag_name in HTMLfun.__format_tags:
            return '\n'

        if tag_name in HTMLfun.__style_tags:
            return ' '

        if tag_name in HTMLfun.__table_tags:
            return {'table': '\n\n', 'tbody': '',
                    'th': '\n', 'tr': '\n',
                    'td': '    '}[tag_name]

        if tag_name == 'table':
            return '\n'

        if tag_name in HTMLfun.__list_tags:
            return ''

        raise CallError(f"Unspecified tag ('{tag_name}'), was HTML sanitize before calling this function?")


    __allowed_tags = __header_tags + __format_tags + __style_tags + __table_tags + __list_tags

    class Stat:
        def __init__(self, orgi_text_len: int):
            self.orgi_text_len = orgi_text_len
            self.sani_text_len = None
            self.tags_cut = {}
            self.tags_cut_total = 0

        def hprint(self):
            print(f'Len change: {self.orgi_text_len} => {self.sani_text_len}: ')
            print(f'Cut ratio: {self.cut_ratio()}')
            print(f'Mod tags: {len(self.tags_cut)} => {self.tags_cut_total}')

        def openFeed(text: str):
            return HTMLfun.Stat(len(text))

        def feedTagMod(self, tag_name: str):
            if tag_name in self.tags_cut:
                self.tags_cut[tag_name] += 1
            else:
                self.tags_cut[tag_name] = 1

            self.tags_cut_total += 1
        def closeFeed(self, output_text: str):
            self.sani_text_len = len(output_text)

            return self
        def cut_ratio(self):
            if self.orgi_text_len == 0:
                return 0

            return 100 * (1 - (self.sani_text_len / self.orgi_text_len))

    @staticmethod
    def sanitize(html: str, purge_classes: bool = False, purge_styles: bool = False, start_hlevel: int = None) -> str:
        # Parse the HTML content
        soup = BeautifulSoup(html, 'html.parser')
        stat = HTMLfun.Stat.openFeed(html)

        trans_hlevel_vector = {}
        prev_tag = soup.new_tag('<b>NULL TAG</b>')

        # Find all tags in the HTML content
        for tag in soup.find_all(True):
            # remove tag that is not in 'Allowed Tags' list
            if not (tag.name in HTMLfun.__allowed_tags):
                tag.unwrap()  # Remove the tag but keep its contents
                stat.feedTagMod(tag.name)
                continue

            if purge_classes and 'class' in tag.attrs:
                del tag.attrs['class']

            if purge_styles and 'style' in tag.attrs:
                del tag.attrs['style']

            if tag.name in HTMLfun.__style_tags:
                # if style element that does not hold text, remove it:
                if len(tag.contents) == 0:
                    tag.unwrap()
                    tag = prev_tag
                # if previous element is a previus tag and tag name is the same,
                # then merge tags
                elif prev_tag == tag.previous_sibling and prev_tag.name == tag.name:
                    new_tag = soup.new_tag(tag.name)
                    new_tag.extend(prev_tag.contents + tag.contents)
                    tag.insert_after(new_tag)
                    tag.decompose()
                    prev_tag.decompose()

                    tag = new_tag

            elif start_hlevel != None and tag.name in HTMLfun.__header_tags:
                if tag.name not in trans_hlevel_vector:
                    if (int)(tag.name[1]) < start_hlevel:
                        trans_hlevel_vector[tag.name] = 'h' + (str)(start_hlevel)
                    elif len(trans_hlevel_vector) == 0:
                        trans_hlevel_vector[tag.name] = 'h' + start_hlevel
                    else:
                        new_h_list = list(trans_hlevel_vector.values())[-1]
                        trans_hlevel_vector[tag.name] = 'h' + (str)((int)(new_h_list[1]) + 1)

                tag.name = trans_hlevel_vector[tag.name]

            prev_tag = tag

        output_str = str(soup).strip()
        return output_str, stat.closeFeed(output_str)


    @staticmethod
    def sanitize_html(html_descr: HTMLDescription, lang = None):
        html_text = html_descr.text(lang=lang)

        html_text_out, stat = HTMLfun.sanitize(html_text, start_hlevel = 2)

        html_descr.text(text = html_text_out, lang = lang)

        return stat

    @staticmethod
    def getStripedText(html) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()
        #transf = {'p': '\n\n', 'br': '\n', 'hr': '-' * 64, 'li': ' - '}

    # prototype function
    # begin
    # continus begin
    # end
    # continuus end
    # all
    def cut_head(html: str, inline_tags: str = [], text_pattern: str = None, seek = False, cut_pattern = True):
        soup = BeautifulSoup(html, 'html.parser')
        stat = HTMLfun.Stat.openFeed(html)

        p_parent = None
        l_tag = None
        tags_for_removal = []
        parent_text = ''

        for tag in soup.find_all(True):
            # ignore breaks
            if tag.name == 'br':
                continue

            # clean up any encounted empty tag
            if len(tag.text) == 0:
                tags_for_removal.append(tag)
                continue

            if tag.name == 'p' and len(parent_text) == 0:
                if p_parent != None:
                    tags_for_removal.append(p_parent)

                p_parent = tag
                parent_text = tag.text
            elif tag.name in inline_tags:
                if parent_text.startswith(tag.text) == False:
                    break

                parent_text = parent_text[len(tag.text):]

                if text_pattern != None:
                    if text_pattern.startswith(tag.text) == False:
                        break
                    text_pattern = text_pattern[len(tag.text):]

                if len(parent_text) == 0:
                    tags_for_removal.append(p_parent)
                    p_parent = None

                tags_for_removal.append(tag)

                if text_pattern != None and len(text_pattern) == 0:
                    # patter has been found, done.
                    break
            else:
                l_tag = tag
                break

        # if there is a single element in input 'l_tag' stays as 'None'
        # but we still want to validate if this single tag is not the one for removal
        if p_parent != None and \
                (l_tag != None and p_parent != l_tag.parent) and \
           p_parent.text == text_pattern:
            tags_for_removal.append(p_parent)

        for tag in tags_for_removal:
            stat.feedTagMod(tag.name)
            tag.extract()

        output_str = str(soup).strip()
        return output_str, stat.closeFeed(output_str)

    class PartialVRank:
        factor = -1
        def __init__(self, compl: int, len: int):
            self.compl = compl
            self.len = len

        def iamPerfect(self):
            HTMLfun.PartialVRank.factor = (self.len * 100) / self.compl
        def norm(self):
            return round ((self.compl * HTMLfun.PartialVRank.factor)/self.len)


    def variety_partialrank(html: str) -> int:
        soup = BeautifulSoup(html, 'html.parser')
        prev_tag = ''
        rank = 0

        # Find all tags in the HTML content
        for tag in soup.find_all(True):
            if tag.name != prev_tag:
                rank += 2
            else:
                rank += 1

        return HTMLfun.PartialVRank(rank, len(html))
