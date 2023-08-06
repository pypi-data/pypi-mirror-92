from typing import Dict, Generator, ValuesView, TYPE_CHECKING

from collections import defaultdict
import statistics
#from pdf2txt.tokens_filtering import LineList
from pdf2txt.exceptions import ParagraphNotFoundError
#from backup.paragraph_list import ParagraphList
import numpy as np
import re
from enum import Enum

if TYPE_CHECKING:
    from pdf2txt.core import Document, Token




def extract(textlines):

        if len(textlines)<=2:
            return [textlines]

        # normalizing the line gaps to get an average gap for detetcting the paraagarphs
        line_gap_list=[j[0].bottom-i[0].bottom+(1+j[0].is_bold)*j[0].font_size for i, j in zip(textlines[:-1], textlines[1:])]
#        line_gap_list = [line.space_above+line.tokens[0].font_size for line in textlines if line.space_above != -1]
        if len(line_gap_list)<len(textlines):
            line_gap_list.insert(0,max(line_gap_list) if len(line_gap_list) else 0)
        #	curr_line=[line.Text for line in textlines]

        if len(line_gap_list) <= 3:
            return [textlines]

        # Now we need the 2nd order derivative so that we can  get the
        # global maxima to get the paragraphs
        # 2nd order derivative is defined as :
        # f(x+1,y) + f(x-1,y) -2*f(x,y) ----> in the x direction
        # f(x,y+1) + f(x,y-1) -2*f(x,y) ----> in the y direction
        # we only need the derivative in the y direction here

        derivative_line_gap = line_gap_list
        for i in range(0, len(line_gap_list) - 1):
            derivative_line_gap[i] = line_gap_list[i] + line_gap_list[i + 1] - 2 * line_gap_list[i]

        # removing outliers
        outlier_cut_off = statistics.stdev(derivative_line_gap)
        derivative_line_gap2 = [d for d in derivative_line_gap if abs(d) < 2*outlier_cut_off]
        cut_off = 0.9*statistics.stdev(derivative_line_gap2)
        if cut_off < 2:
            return [textlines]

        #	cut_off=statistics.stdev(derivative_line_gap)

        derivative_line_gap = list(map(lambda x: 0 if abs(x) < cut_off else x, derivative_line_gap))

        zero_crossings = np.where(np.diff(np.sign(derivative_line_gap)) == -2)[0]+1
        zero_crossings = zero_crossings.tolist()

        # checkjing how many are there with a line gap of less than 1
        # forming the paragraph:
        if 2 in zero_crossings:
            zero_crossings.remove(2)
        if len(zero_crossings) == 0:
            return [textlines]

        # split array in ranges
        for i in range(len(zero_crossings)):
            if zero_crossings[i] == i:
                zero_crossings[i] = i + 1
        zero_crossings.insert(0, 0)
        zero_crossings.insert(len(zero_crossings), len(textlines))

        paragraph_ranges = [(zero_crossings[i], zero_crossings[i + 1]) for i in range(len(zero_crossings) - 1)]
        paragraphs= [textlines[i:j] for i, j in paragraph_ranges]

        return paragraphs


def extract2(textlines):
    if len(textlines) <= 2:
        return [textlines]

    # normalizing the line gaps to get an average gap for detetcting the paraagarphs
    line_gap_list = [j[0].bottom - i[0].bottom + j[0].font_size for i, j in
                     zip(textlines[:-1], textlines[1:])]
    #        line_gap_list = [line.space_above+line.tokens[0].font_size for line in textlines if line.space_above != -1]
    if len(line_gap_list) < len(textlines):
        line_gap_list.insert(0, max(line_gap_list) if len(line_gap_list) else 0)
    #	curr_line=[line.Text for line in textlines]

    if len(line_gap_list) <= 3:
        return [textlines]

    # Now we need the 2nd order derivative so that we can  get the
    # global maxima to get the paragraphs
    # 2nd order derivative is defined as :
    # f(x+1,y) + f(x-1,y) -2*f(x,y) ----> in the x direction
    # f(x,y+1) + f(x,y-1) -2*f(x,y) ----> in the y direction
    # we only need the derivative in the y direction here

    derivative_line_gap = line_gap_list
    for i in range(0, len(line_gap_list) - 1):
        derivative_line_gap[i] = line_gap_list[i] + line_gap_list[i + 1] - 2 * line_gap_list[i]

    # removing outliers
    outlier_cut_off = statistics.stdev(derivative_line_gap)
    derivative_line_gap2 = [d for d in derivative_line_gap if abs(d) < 2 * outlier_cut_off]
    cut_off = 0.9 * statistics.stdev(derivative_line_gap2)
    if cut_off < 2:
        return [textlines]

    #	cut_off=statistics.stdev(derivative_line_gap)

    derivative_line_gap = list(map(lambda x: 0 if abs(x) < cut_off else x, derivative_line_gap))

    zero_crossings = np.where(np.diff(np.sign(derivative_line_gap)) == -2)[0] + 1
    zero_crossings = zero_crossings.tolist()

    # checkjing how many are there with a line gap of less than 1
    # forming the paragraph:
    if 2 in zero_crossings:
        zero_crossings.remove(2)
    if len(zero_crossings) == 0:
        return [textlines]

    # split array in ranges
    for i in range(len(zero_crossings)):
        if zero_crossings[i] == i:
            zero_crossings[i] = i + 1
    zero_crossings.insert(0, 0)
    zero_crossings.insert(len(zero_crossings), len(textlines))

    paragraph_ranges = [(zero_crossings[i], zero_crossings[i + 1]) for i in range(len(zero_crossings) - 1)]
    paragraphs = [textlines[i:j] for i, j in paragraph_ranges]

    return paragraphs



class ContentType(Enum):
    Text=1
    Table=2
    Graph=3

class Paragraph:
    """
    A continuous group of tokens within a document.

    A paragraph is intended to label a group of tokens. Said tokens must be continuous
    in the document.

    Warning:
        You should not instantiate a PDFParagraph class yourself, but should call
        `create_paragraph` from the `PDFParagraphing` class below.

    Args:
        document (PDFDocument): A reference to the document.
        name (str): The name of the paragraph.
        unique_name (str): Multiple paragraphs can have the same name, but a unique name
            will be generated by the PDFParagraphing class.
        start_token (PDFToken): The first token in the paragraph.
        end_token (PDFToken): The last token in the paragraph.
    """

    document: "Document"
    name: str
    unique_name: str
    start_token: "Token"
    end_token: "Token"

    def __init__(self, document, name, unique_name):
        self.document = document
        self.name = name
        self.unique_name = unique_name
        self.title = None

    @property
    def content(self):
        if not hasattr(self, "_content"):
            self._content=[]

        return self._content


    def add_content(self, content, type):

        self.content.append({'type':type, 'content':content})

    @property
    def Text(self):
        return_str=""
        if self.title:
            return_str = ' '.join([t.Text for t in self.title]) + '\n'
            return_str += '-' * len(return_str)
        for content in self.content:
            if content["type"]==ContentType.Text:
                return_str += '\n' + ' '.join([c.Text for c in content["content"]])
            elif content["type"]==ContentType.Graph:
                return_str+="<START GRAPH DATA>\n"
                return_str+='\n'+content["content"].to_string(index=False)
                return_str+="\n<END GRAPH DATA>"
            elif content["type"]==ContentType.Table:
                return_str+="\n<START TABLE>\n"
                return_str+='\n'+content["content"].to_string(index=False)
                return_str+="\n<END TABLE>"
        return return_str


    def __eq__(self, other: object) -> bool:
        """
        Returns True if the two paragraphs have the same unique name and are from the
        same document
        """
        if not isinstance(other, Paragraph):
            raise NotImplementedError(f"Can't compare PDFParagraph with {type(other)}")
        return all(
            [
                self.document == other.document,
                self.unique_name == other.unique_name,
                self.start_token == other.start_token,
                self.end_token == other.end_token,
                self.__class__ == other.__class__,
            ]
        )

    def __len__(self):
        """
        Returns the number of tokens in the paragraph.
        """
        return len(self.text_lines)
    @property
    def text_lines(self):
        if hasattr(self, "_text_lines"):
            return self._text_lines

        self._text_lines=[c for c in self.content if c["type"]==ContentType.Text]
        return self._text_lines

    def __repr__(self):
        return (
            f"<PDFParagraph name: '{self.name}', unique_name: '{self.unique_name}', "
            f"number of tokens: {len(self)}>"
        )
    def filter_by_text_contains(self, texts: str, filter_type='any', case_sensitive=True, substring_match=False):
        """
        Filter for tokens whose text contains the given string.

        Args:
            text (str): The text to filter for.

        Returns:
            LineList: The filtered list.
        """
        flags = re.MULTILINE
        if not case_sensitive:
            flags |= re.IGNORECASE
        regex_str='|'.join(texts)
        regex_str=r'\b('+regex_str+')'
        regex = re.compile(regex_str, flags=flags)

        if filter_type=='any' or len(texts)==1:
            lines = [line['content'] for line in self.text_lines if regex.search('\n'.join([token.Text for token in line['content']]))]
        elif filter_type=='all':
            lines = [line for line in self.text_lines if all(x in self.Text for x in texts)]
        else:
            raise Exception("Unknown filter type. Should be: 'any' or 'all'")


        return lines


class Paragraphs:
    """
    A paragraphing utilities class, made available on all PDFDocuments as ``.paragraphing``.
    """

    document: "Document"
    name_counts: Dict[str, int]
    paragraphs_dict: Dict[str, Paragraph]

    def __init__(self, document: "Document"):
        self.paragraphs_dict = {}
        self.name_counts = defaultdict(int)
        self.document = document

    def create_paragraph(  self, name=None):
        """
        Creates a new paragraph with the specified name.

        Creates a new paragraph with the specified name, starting at `start_token` and
        ending at `end_token` (inclusive). The unique name will be set to name_<idx>
        where <idx> is the number of existing paragraphs with that name.

        Args:
            name (str): The name of the new paragraph.
            start_token (PDFToken): The first token in the paragraph.
            end_token (PDFToken): The last token in the paragraph.
            include_last_token (bool): Whether the end_token should be included in
                the paragraph, or only the tokens which are strictly before the end
                token. Default: True (i.e. include end_token).

        Returns:
            Paragraph: The created paragraph.

        Raises:
            InvalidPDFParagraphError: If a the created paragraph would be invalid. This is
                usually because the end_token comes after the start token.
        """
        if name==None:
            name="paragraph"+str(len(self.document.paragraphs.paragraphs))
        current_count = self.name_counts[name]
        unique_name = f"{name}_{current_count}"
        self.name_counts[name] += 1

        paragraph = Paragraph(self.document, name, unique_name)
        self.paragraphs_dict[unique_name] = paragraph
        return paragraph

    def get_paragraphs_with_name(self, name: str) -> Generator[Paragraph, None, None]:
        """
        Returns a list of all paragraphs with the given name.
        """
        return (
            self.paragraphs_dict[f"{name}_{idx}"]
            for idx in range(0, self.name_counts[name])
        )

    def get_paragraph(self, unique_name: str) -> Paragraph:
        """
        Returns the paragraph with the given unique name.

        Raises:
            PDFParagraphNotFoundError: If there is no paragraph with the given unique_name.
        """
        try:
            return self.paragraphs_dict[unique_name]
        except KeyError as err:
            raise ParagraphNotFoundError(
                f"Could not find paragraph with name {unique_name}"
            ) from err

    @property
    def paragraphs(self) -> ValuesView[Paragraph]:
        """
        Returns the list of all created PDFParagraphs.
        """
        return self.paragraphs_dict.values()


    def filter_by_title_equal(self, text: str):
        """
        Filter for tokens whose text is exactly the given string.

        Args:
            text (str): The text to filter for.
            stripped (bool, optional): Whether to strip the text of the token before
                comparison. Default: True.

        Returns:
            LineList: The filtered list.
        """

        return [paragraph for paragraph in self.paragraphs_dict.values() if paragraph.title == text]

    def filter_by_title_contains(self, text: str):
        """
        Filter for tokens whose text contains the given string.

        Args:
            text (str): The text to filter for.

        Returns:
            LineList: The filtered list.
        """


        paragraphs= [paragraph for paragraph in self.paragraphs_dict.values() if paragraph.title is not None and text in paragraph.title.Text]


        return paragraphs

    def filter_by_text_contains(self, texts: str, filter_type='any', case_sensitive=True, substring_match=False):
        """
        Filter for tokens whose text contains the given string.

        Args:
            text (str): The text to filter for.

        Returns:
            LineList: The filtered list.
        """
        flags = re.MULTILINE
        if not case_sensitive:
            flags |= re.IGNORECASE
        texts=[re.escape(t) for t in texts]
        regex_str='|'.join(texts)
        regex_str=r'\b('+regex_str+')'
        regex = re.compile(regex_str, flags=flags)

        if filter_type=='any' or len(texts)==1:
            paragraphs = [paragraph for paragraph in self.paragraphs_dict.values() if regex.search(paragraph.Text)]
        elif filter_type=='all':
            paragraphs=[paragraph for paragraph in self.paragraphs_dict.values() if all(x in paragraph.Text for x in texts)]
        else:
            raise Exception("Unknown filter type. Should be: 'any' or 'all'")





        return paragraphs


    def filter_by_text_matches_regex(self, regex_str, case_sensitive=True):
        """
        Filter for tokens whose text contains the given string.

        Args:
            text (str): The text to filter for.

        Returns:
            LineList: The filtered list.
        """
        flags = re.MULTILINE
        if not case_sensitive:
            flags |= re.IGNORECASE

        regex = re.compile(regex_str, flags=flags)

        paragraphs = [paragraph for paragraph in self.paragraphs_dict.values() if regex.search(paragraph.Text)]

        return paragraphs


    def get_last_paragraph(self):
        if len(self.paragraphs_dict.values())==0:
            return None
        return list(self.paragraphs_dict.values())[-1]