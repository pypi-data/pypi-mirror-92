from django.template import Library, Node
from django.utils.encoding import force_text

register = Library()


def strip_spaces_in_tags(value):
    return force_text(value).replace(" ", "").replace("\n", "")


class NoSpacesNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return strip_spaces_in_tags(self.nodelist.render(context).strip())


@register.tag
def nospaces(parser, token):
    """Remove all whitespace from tags and text.

    {% spaceless %} does a similar thing, but only between tags.

    Example:
        {% nospaces %}
            <strong>
                Hello
                this is text
            </strong>
        {% nospaces %}

    Returns:
        <strong>Hello this is text</strong>
    """
    nodelist = parser.parse(("endnospaces",))
    parser.delete_first_token()
    return NoSpacesNode(nodelist)
