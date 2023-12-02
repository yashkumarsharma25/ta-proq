from marko import Markdown
from marko.md_renderer import MarkdownRenderer

def dictify(content):
    '''Converts the markdown text to dictionaries based on heading outline.'''

    def nest_blocks(blocks, level):
        current_block = None
        inner_blocks = {}
        for block in blocks:
            if block.get_type() == "Heading" and block.level == level:
                current_block = block.children[0].children
                inner_blocks[current_block] = []
            elif current_block:
                inner_blocks[current_block].append(block)
        if not current_block:
            renderer= MarkdownRenderer()
            return "".join(renderer.render(block) for block in blocks)
        return {block_name: nest_blocks(children,level+1) for block_name,children in inner_blocks.items()}

    document = Markdown().parse(content)
    return nest_blocks(document.children,1)

