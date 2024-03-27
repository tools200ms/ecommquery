from bs4 import BeautifulSoup

# String operations:
class StringOp:
    __allowed_tags = ['p', 'b', 'i', 'strong', 'em', 'u',
                      'table', 'tbody', 'th', 'tr', 'td',
                      'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
                      'ul', 'ol', 'li',
                      'br']

    def sanitize_html(html: str, purge_classes: bool = False, purge_style: bool = False) -> str:
        # Parse the HTML content
        soup = BeautifulSoup(html, 'html.parser')

        # Find all tags in the HTML content
        for tag in soup.find_all(True):
            # remove tag that is not in 'Allowed Tags' list
            if tag.name not in StringOp.__allowed_tags:
                tag.unwrap()  # Remove the tag but keep its contents
                continue

            if purge_classes and 'class' in tag.attrs:
                del tag.attrs['class']

            if purge_style and 'style' in tag.attrs:
                del tag.attrs['style']

        return str(soup).strip()

    # prototype function
    # begin
    # continus begin
    # end
    # continuus end
    # all
    def trim_tags(html: str, tags: [], mode = None):
        soup = BeautifulSoup(html, 'html.parser')

        level = 0
        p_parent = None
        p_parent_for_removal = False
        tags_for_removal = []

        for tag in soup.find_all(True):
            if tag.name == 'p':
                p_parent = tag
                p_parent_for_removal = True
                continue
            elif tag.name == 'b' and p_parent != None:
                tags_for_removal.append(tag)
                if p_parent_for_removal:
                    tags_for_removal.append(p_parent)
                    p_parent_for_removal = False
            else:
                break

        for tag in tags_for_removal:
            tag.extract()

        p_parent = None
        p_parent_for_removal = False
        tags_for_removal = []

        for tag in soup.find_all(True):
            if tag.name == 'h2':
                tag.get_text().strip().lower() == 'opis produktu'
                tags_for_removal.append(tag)
            else:
                break

        for tag in tags_for_removal:
            tag.extract()

        return str(soup).strip()