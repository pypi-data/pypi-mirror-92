from . import tag_parse_ruby
from . import tag_parse_migaku_ja

import math
import codecs
import cchardet as chardet
import pysubs2
from PyQt5.QtGui import QFont, QFontMetrics, QGuiApplication


def strip_ass_tags(text):
    ret = ''
    in_curly = False
    for c in text:
        if c == '{':
            in_curly = True
        elif c == '}':
            in_curly = False
        elif not in_curly:
            ret += c
    return ret


class RubySubParser():

    def __init__(self, frame_width, frame_height, bottom_margin, font_name, font_size, ruby_font_size, bold, tag_parser=tag_parse_ruby.parse):

        self.tag_parser = tag_parser

        # ASS font height is actually the line height, not the cap height like regularly
        probe_size = 1000
        probe_font = QFont(font_name, probe_size)
        probe_font.setBold(bold)
        probe_font_metrics = QFontMetrics(probe_font)
        ass_font_factor = probe_font_metrics.capHeight() / probe_font_metrics.lineSpacing()

        self.normal_line_height = round(font_size)
        self.font_size = round(font_size * ass_font_factor)
        
        if ruby_font_size is None:
            self.ruby_font_size = round(font_size / 2)
        else:
            self.ruby_font_size = round(ruby_font_size * ass_font_factor)

        font = QFont(font_name, self.font_size)

        font.setBold(bold)
        self.font_metrics = QFontMetrics(font)
        self.font_height = self.font_metrics.height()

        ruby_font = QFont(font_name, self.ruby_font_size)
        ruby_font.setBold(bold)
        self.ruby_font_metrics = QFontMetrics(ruby_font)
        self.ruby_font_height = self.ruby_font_metrics.height()

        self.frame_width = frame_width
        self.sub_origin = math.floor(frame_height - (font_size/2 + bottom_margin))

    def get_line_height(self, line):
        for (_, ruby_txt) in line:
            if ruby_txt:
                return math.floor(self.normal_line_height * 1.5)
        return self.normal_line_height

    def parse_sub(self, sub):
        sub = sub.replace('\\N', '\n')

        parsed_lines = self.tag_parser(sub)

        # Calculate line y positions
        # The origin of y positions is the center of the main line
        line_y_positions = [self.sub_origin]
        for line in parsed_lines[-1:0:-1]:
            line_y_positions.insert(0, line_y_positions[0] - self.get_line_height(line))

        # Process lines
        ret = []

        for line, y in zip(parsed_lines, line_y_positions):

            # Calculate part and line width
            widths = []

            for (txt, ruby_txt) in line:
                txt_no_tags = strip_ass_tags(txt)
                ruby_txt_no_tags = strip_ass_tags(ruby_txt)

                txt_width = self.font_metrics.horizontalAdvance(txt_no_tags)
                ruby_txt_width = self.ruby_font_metrics.horizontalAdvance(ruby_txt_no_tags)

                widths.append(max(txt_width, ruby_txt_width))

            line_width = sum(widths)

            ruby_y = math.floor(y - self.font_height/2 - self.ruby_font_size/2)

            # Always at left side of current part
            curr_x = round(self.frame_width/2 - line_width/2)

            for ((txt, ruby_txt), width) in zip(line, widths):
                # Center of current part
                x = round(curr_x + width/2)

                # Highlight test
                import random
                if False and random.randint(0, 6) == 0 and len(txt) > 1:
                    c = '00ffff'
                    x1 = curr_x
                    x2 = curr_x + width
                    y1 = math.ceil(y + self.font_height/2)
                    y2 = math.ceil(y1 - (self.font_height*1.4 if ruby_txt else self.font_height))
                    ret.append( (0, 'Highlight', '{\\pos(0,0)}{\c&H%s&\\1a&H80&}{\p1}m %d %d l %d %d %d %d %d %d{\p0}{\c\\1a}' % (c, x1, y1, x2, y1, x2, y2, x1, y2)) )
                
                # Underline test
                if False and random.randint(0, 4) == 0 and ruby_txt:
                    c = '4e4ef1'
                    if random.randint(0, 1) == 0:
                        c = '4ebbf1'

                    x1 = curr_x
                    x2 = curr_x + width
                    y1 = math.ceil(y + self.font_height/2)
                    y2 = math.ceil(y1 + self.font_height*0.075)

                    ret.append( (1, 'Underline', '{\\pos(0,0)}{\c&H%s&}{\p1}m %d %d l %d %d %d %d %d %d{\p0}{\c}' % (c, x1, y1, x2, y1, x2, y2, x1, y2)) )

                if txt.strip():
                    ret.append( (3, 'Default', '{\\pos(%d,%d)}%s' % (x, y, txt)) )

                if ruby_txt.strip():
                    ret.append( (2, 'Ruby', '{\\pos(%d,%d)}%s' % (x, ruby_y, ruby_txt)) )

                curr_x += width

        return ret


def convert_sub_file(in_path, out_path, tag_parser=tag_parse_ruby.parse):

    # Determine encoding
    f = open(in_path, 'rb')
    subs_data = f.read()
    f.close()

    boms_for_enc = [
        ('utf-32',      (codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)),
        ('utf-16',      (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)),
        ('utf-8-sig',   (codecs.BOM_UTF8,)),
    ]

    for enc, boms in boms_for_enc:
        if any(subs_data.startswith(bom) for bom in boms):
            subs_encoding = enc
            break
    else:
        chardet_ret = chardet.detect(subs_data)
        subs_encoding = chardet_ret['encoding']

    # Load subs
    with open(in_path, encoding=subs_encoding, errors='replace') as f:
        subs = pysubs2.SSAFile.from_file(f)

    # Order subs
    subs.sort()

    # Determine frame size
    frame_width = int(subs.info.get('PlayResX', '1920'))
    frame_height = int(subs.info.get('PlayResY', '1080'))

    bottom_margin = round(frame_height * 0.04)

    # Create styles
    style = subs.styles.get('Default')
    if style is None:
        # Todo: Set nice default style if Default is not found
        style = pysubs2.SSAStyle()
    else:
        bottom_margin = round(style.marginv)

    style.fontsize = math.floor(style.fontsize)
    style.italic = False
    style.underline = False
    style.strikeout = False
    style.scalex = 100.0
    style.scaley = 100.0
    style.spacing = 0.0
    style.angle = 0.0
    style.alignment = 5     # Center alignment
    style.marginl = 0
    style.marginr = 0
    style.marginv = 0

    ruby_style = style.copy()
    ruby_style.fontsize = math.floor(style.fontsize / 2)

    underline_style = style.copy()
    underline_style.alignment = 7   # Top-left alignment

    highlight_style = style.copy()
    highlight_style.outline = 0
    highlight_style.shadow = 0
    highlight_style.alignment = 7   # Top-left alignment

    subs.styles.clear()
    subs.styles['Default'] = style
    subs.styles['Ruby'] = ruby_style
    subs.styles['Underline'] = underline_style
    subs.styles['Highlight'] = highlight_style

    font_name = style.fontname
    font_size = style.fontsize
    ruby_font_size = ruby_style.fontsize
    bold = style.bold
    
    parser = RubySubParser(frame_width, frame_height, bottom_margin, font_name, font_size, ruby_font_size, bold, tag_parser)


    # Create parsed subtitle events
    original_events = subs.events.copy()
    subs.events.clear()

    for e in original_events:
        parts = parser.parse_sub(e.text)
        for (layer, style, text) in parts:
            e = e.copy()
            e.layer = layer
            e.style = style
            e.text = text
            subs.events.append(e)

    subs.save(out_path, header_notice='Generated by rubysubs')



def main():
    import sys
    
    if len(sys.argv) not in [3, 4]:
        print('Usage: %s <source subtitle> <output subtitle> [tag parser]' % sys.argv[0])
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2]

    if len(sys.argv) >= 4:
        tag_parser_requested = sys.argv[3].lower()

        tag_parsers = {
            'ruby': tag_parse_ruby.parse,
            'ja':   tag_parse_migaku_ja.parse,
        }

        if not tag_parser_requested in tag_parsers:
            print('Invalid tag parser.')
            sys.exit(1)

        tag_parser = tag_parsers[tag_parser_requested]
    else:
        tag_parser = tag_parse_ruby.parse

    # Required for QFontMetrics
    qapp = QGuiApplication(sys.argv)

    convert_sub_file(in_path, out_path, tag_parser)

    sys.exit(0)


if __name__ == "__main__":
    main()
