import re
import argparse
import fileinput
import jaconv
import sys

from kuro2sudachi.normalizer import SudachiCharNormalizer


parser = argparse.ArgumentParser(
    description="convert kuromoji user dict to sudacchi user dict"
)
parser.add_argument("file", help="kuromoji dict file path")
parser.add_argument("-o", "--out", help="output path")
parser.add_argument(
    "-r", "--rewrite", help="rewrite text file path (default: ./rewrite.def)"
)
parser.add_argument("--ignore", action='store_true',
                    help="ignore unsupported pos error")

pos_dict = {
    "固有名詞": "名詞,固有名詞,一般,*,*,*",
    "名詞": "名詞,普通名詞,一般,*,*,*",
    "形容詞": "形容詞,一般,*,*,*,*",
    "副詞": "副詞,*,*,*,*,*",
    "動詞": "動詞,一般,*,*,*,*",
    "記号": "記号,一般,*,*,*,*",
}

p = re.compile("[\u30A1-\u30FC]*")


class Error(Exception):
    pass


class UnSupportedPosError(Error):
    pass


class DictFormatError(Error):
    pass


def nomlized_yomi(yomi: str) -> str:
    yomi = jaconv.hira2kata(yomi)
    if p.fullmatch(yomi):
        return yomi
    else:
        return ""
    return ""


def pos_convert(pos: str) -> str:
    try:
        spos = pos_dict[pos]
        return spos
    except KeyError:
        raise UnSupportedPosError(f"{pos} is not supported pos")


def convert(line: str, rewrite="rewrite.def") -> str:
    data = line.split(",")
    try:
        word = data[0]
        # splited = data[1]
        yomi = nomlized_yomi(data[2])
        pos = pos_convert(data[3])
    except IndexError:
        raise DictFormatError(f"{line} is invalid format")

    normalizer = SudachiCharNormalizer(rewrite_def_path=rewrite)
    normalized = normalizer.rewrite(word)
    return f"{normalized},4786,4786,5000,{word},{pos},{yomi},{word},*,*,*,*,*"


def cli() -> str:
    args = parser.parse_args()
    out = open(args.out, "wt")
    with fileinput.input(files=args.file) as input:
        for line in input:
            line = line.strip()
            if line == "":
                continue
            rewrite = args.rewrite
            converted = ""
            try:
                converted = convert(line, rewrite)
            except UnSupportedPosError as e:
                if args.ignore:
                    continue
                else:
                    raise e

            out.write(f"{converted}\n")
