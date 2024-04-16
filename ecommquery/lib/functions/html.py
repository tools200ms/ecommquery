from bs4 import BeautifulSoup

from ecommquery.lib.atomic.description import HTMLDescription


# String operations:
class HTMLfun:
    __header_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    __style_tags = ['b', 'i', 'strong', 'em', 'u']
    __table_tags = ['table', 'tbody', 'th', 'tr', 'td']
    __list_tags = ['ul', 'ol', 'li']

    __allowed_tags = ['p'] + __header_tags + __style_tags + __table_tags + __list_tags + ['br']

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
    def sanitize(html: str, purge_classes: bool = False, purge_style: bool = False, start_hlevel: int = None) -> str:
        # Parse the HTML content
        soup = BeautifulSoup(html, 'html.parser')
        stat = HTMLfun.Stat.openFeed(html)

        trans_hlevel_vector = {}

        # Find all tags in the HTML content
        for tag in soup.find_all(True):
            # remove tag that is not in 'Allowed Tags' list
            if tag.name not in HTMLfun.__allowed_tags:
                tag.unwrap()  # Remove the tag but keep its contents
                stat.feedTagMod(tag.name)
                continue

            if purge_classes and 'class' in tag.attrs:
                del tag.attrs['class']

            if purge_style and 'style' in tag.attrs:
                del tag.attrs['style']

            if start_hlevel != None and tag.name in HTMLfun.__header_tags:
                if (int)(tag.name[1]) < start_hlevel:
                    trans_hlevel_vector[tag.name] = 'h' + (str)(start_hlevel)
                    tag.name = 'h' + (str)(start_hlevel)
                elif len(trans_hlevel_vector) != 0:
                    if tag.name not in trans_hlevel_vector:
                        l_h = list(trans_hlevel_vector.keys())[-1]
                        n_h = trans_hlevel_vector[l_h]
                        trans_hlevel_vector[tag.name] = 'h' + (str)((int)(n_h[1]) + 1)

                    tag.name = trans_hlevel_vector[tag.name]



        output_str = str(soup).strip()
        return output_str, stat.closeFeed(output_str)

    @staticmethod
    def sanitize_descr(html_descr: HTMLDescription, lang = None):
        html_text = html_descr.text(lang=lang)

        html_text_out, stat = HTMLfun.sanitize(html_text, start_hlevel = 2)

        html_descr.text(text = html_text_out, lang = lang)

        return stat

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
