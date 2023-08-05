"""
This sub module contains the BaseLink class and its child classes Link,
LibraryLink, WebLink, and Image. Instead of constructing a Link, LibraryLink,
or WebLink use `make_link`. This will return the correct object type.
Image is used only for displaying images i.e. links that start with an !. For
a reference to an image use `make_link`.
"""

# Testing for this module is handled by test_buildup rather than directly running
# the functions as it provides a more realisic running of the objects.

import os
import regex as re
import logging
from dataclasses import dataclass
from marshmallow import Schema, fields, post_load, pre_load, ValidationError
from gitbuilding.buildup.files import FileInfo
from gitbuilding.buildup.quantity import Quantity
from gitbuilding.buildup.utilities import clean_id

_LOGGER = logging.getLogger('BuildUp')

@dataclass
class LinkData:
    """
    A simple data class for the BuildUp data stored with a link
    the input data is validated by a marshmallow schema. This class
    has an extra validation step to check that data isn't defined for
    the wrong type of link.
    """
    category: str
    qty: Quantity
    total_qty: Quantity
    note: str
    step: bool
    output: bool
    bom: bool

    @property
    def part(self):
        """
        Read-only property to check if the part is a part link. This is
        true if the link data does not specify that the link is a step or
        output link.
        """
        return not (self.step or self.output or self.bom)

    @property
    def valid(self):
        """
        Read-only that returns true if the data for the part is valid.
        """
        if self.step + self.output + self.bom > 1:
            _LOGGER.warning('Link can be a step, an output, or a BOM, but not more '
                            'than one of these. Ignoring all data.')
            return False
        if self.step:
            if not _all_none([self.category, self.qty, self.total_qty, self.note]):
                _LOGGER.warning('Unexpected properties in step link. Ignoring all data.')
                return False
        if self.output:
            if not _all_none([self.category, self.total_qty, self.note]):
                _LOGGER.warning('Unexpected properties in output link. Ignoring all data.')
                return False
        if self.bom:
            if not _all_none([self.category, self.qty, self.total_qty, self.note]):
                _LOGGER.warning('Unexpected properties in BOM link. Ignoring all data.')
                return False
        return True

def _all_none(values):
    for value in values:
        if value is not None:
            return False
    return True


class LinkDataSchema(Schema):
    """
    This is the schema for the extra data that can be appended on a link
    """
    #pylint: disable=no-self-use
    cat = fields.Str(missing=None, allow_none=True)
    qty = fields.Str(missing=None, allow_none=True)
    totalqty = fields.Str(missing=None, allow_none=True)
    note = fields.Str(missing=None, allow_none=True)
    step = fields.Bool(missing=False)
    output = fields.Bool(missing=False)
    bom = fields.Bool(missing=False)

    @pre_load
    def _remove_extra(self, in_data, **_):
        if not isinstance(in_data, dict):
            return in_data

        extra_args = [key for key in in_data.keys() if key not in self.fields]
        for key in extra_args:
            del in_data[key]
            _LOGGER.warning('Ignoring unknown link data key "%s"',
                            key,
                            extra={'fussy':True})
        return in_data

    @post_load
    def _make_object(self, data, **_):
        if data['qty'] in [None, ""]:
            data['qty'] = None
        else:
            data['qty'] = Quantity(data['qty'])
        if data['totalqty'] in [None, ""]:
            data['total_qty'] = None
        else:
            data['total_qty'] = Quantity(data['totalqty'])
        if data['cat'] is None:
            data['category'] = None
        else:
            data['category'] = data['cat'].lower()
        del data['cat']
        del data['totalqty']
        link_data = LinkData(**data)
        if link_data.valid:
            return link_data
        return None

def _load_link_data(data):
    if data is None:
        return None
    try:
        return LinkDataSchema().load(data)
    except ValidationError as err:
        # Tidy up error string dictionary
        validation_issue = re.sub(r"""[\'\"\[\]\{\}\.]""", "", str(err))
        _LOGGER.warning('Validating link data failed. %s', validation_issue)
        return None

def _fully_normalise_link(url, page):
    """
    in the case that the page is located at 'folder/page.md' and the url is
    '../folder/path.md'. os.path.normpath(url) does not collapse it to 'path.md'
    this will.
    """
    if url == '':
        return ''
    page_dir = os.path.dirname(page)
    joined = os.path.join(page_dir, url)
    joined = os.path.normpath(joined)
    return os.path.relpath(joined, page_dir)

def _complete_ref_style_link(linktext, link_references):
    """
    If this is a reference style link the link location is added
    from the link references
    """
    if link_references is None:
        return ""
    if linktext in link_references:
        ref_index = link_references.index(linktext)
        return link_references[ref_index].raw_linklocation
    return ""

def _is_web_link(linklocation):
    """
    Returns True if the link is a web link not a local link.
    """
    return re.match(r"^(https?:\/\/)", linklocation) is not None

def _is_from_step_link(linklocation):
    """
    Returns True if the link is a web link not a local link.
    """
    return linklocation.strip().lower() == 'fromstep'

def _library_match(linklocation):
    """
    Matches whether the link is to a part in a library:
    Returns a tuple with the library path, the output directory
    for the library and the part name. If not a library link returns
    None
    """
    # match if the part's link is in the format `abc.yaml#abc` or
    # `abc.yml#abc`
    libmatch = re.match(r"^((.+)\.ya?ml)#(.+)$", linklocation)
    if libmatch is None:
        return None
    library_path = libmatch.group(1)
    #The directory the library will write to:
    library_dir = libmatch.group(2)
    part = libmatch.group(3)
    return (library_path, library_dir, part)

@dataclass
class LinkInfo:
    """
    A simple data class for the key information defined for a link.
    Ths mostly exists to aid finding coding errors which cannot be done
    using dictionaries.
    """
    fullmatch: str
    linktext: str
    linklocation: str
    alttext: str
    buildup_data: LinkData

def make_link(link_dict, page, link_type=1, link_references=None):
    """
    Will create the correct link object, either Link, WebLink, or LibraryLink.
    link_type input should be BaseLink.LINK_REF (=0) or BaseLink.IN_LINE_FULL
    (=1 - default) depending on whether the link is a reference or and in-line
    link. If it is a reference style in-line link, the type will automatically
    adjust to BaseLink.IN_LINE_REF (=2).
    """
    link_dict['buildup_data'] = _load_link_data(link_dict['buildup_data'])
    link_info = LinkInfo(**link_dict)
    if link_info.buildup_data is None:
        output = False
        bom = False
    else:
        output = link_info.buildup_data.output
        bom = link_info.buildup_data.bom
    if link_type == BaseLink.LINK_REF:
        if link_info.buildup_data is not None and link_info.buildup_data.qty is not None:
            _LOGGER.warning('Specifying the quantity of a part used in a link reference'
                            'is not permitted. Quantity should be specified in the text.')
            link_info.buildup_data.qty = None
    else:
        if link_info.linklocation == "":
            link_type = BaseLink.IN_LINE_REF
            link_info.linklocation = _complete_ref_style_link(link_info.linktext,
                                                              link_references)

    if not (output or bom):
        if _is_web_link(link_info.linklocation):
            return WebLink(link_info, page, link_type)
        if _is_from_step_link(link_info.linklocation):
            return FromStepLink(link_info, page, link_type)
        lib_match = _library_match(link_info.linklocation)
        if lib_match is not None:
            return LibraryLink(link_info, page, link_type, lib_match)
    return Link(link_info, page, link_type)

class BaseLink():
    """
    A base class for a link. Can is used to do a number of things from completing
    reference style links. Translating links to be relative to different pages
    and generating the output FileInfo objects. Do not use it directly. Use a the
    child class:
    * Image
    or the function
    the function `make_link`. This  will assign the correct type between `Link`,
    `WebLink`, and `LibraryLink`.
    """
    LINK_REF = 0
    IN_LINE_FULL = 1
    IN_LINE_REF = 2

    def __init__(self, link_info, page, link_type):
        self._page = page
        self._link_type = link_type
        self._link_info = link_info

        #Output links can't have a location, this will may change.
        self._check_location()

        #If it is a an inline part link or output it must have a quantity!
        if link_type != self.LINK_REF and (self.is_part or self.is_output):
            if self.buildup_data.qty is None:
                linktype = 'part' if self.is_part else 'output'
                _LOGGER.warning('The %s link for %s has no qty specified.',
                                linktype,
                                self._link_info.linktext)

    def _check_location(self):
        """
        Checks the location is set correctly for the type of BuildUp data specified.
        For example "output" and "bom" links cannot have a location specified.
        """
        #Output links can't have a location, this will may change.
        if not (self.is_output or self.is_bom):
            return

        if self._link_info.linklocation != '':
            if self.is_output:
                _LOGGER.warning('A target should not be specified when defining an'
                                ' output, it will automatically link to this page.')
            else:
                _LOGGER.warning('A target should not be specified when creating a'
                                ' link to a BOM page. The target will be generated'
                                ' automatically')

    def __eq__(self, obj):
        return obj == self._link_info.linktext

    @property
    def page(self):
        """
        The name of the page the link is defined on
        """
        return self._page

    @property
    def fullmatch(self):
        """
        The full regex match for the link in the original BuildUp
        """
        return self._link_info.fullmatch

    @property
    def linktext(self):
        """
        The text inside the square brackets for the link in BuildUp
        """
        return self._link_info.linktext

    @property
    def raw_linklocation(self):
        """The raw input link location. Reference style links have
        location completed"""
        return self._link_info.linklocation

    @property
    def link_rel_to_page(self):
        """
        Link address relative to the BuildUp page
        """
        return _fully_normalise_link(self.raw_linklocation, self._page)

    @property
    def link_rel_to_root(self):
        """
        Location of the link relative to the root BuildUp directory
        """
        location = self.link_rel_to_page
        if location == "":
            return ""
        page_dir = os.path.dirname(self._page)
        root_link = os.path.join(page_dir, location)
        root_link = os.path.normpath(root_link)
        return root_link

    @property
    def location_undefined(self):
        """
        Returns a boolean value stating whether the link is undefined
        """
        return self.link_rel_to_page == ""

    @property
    def alttext(self):
        """
        Returns the alt-text of the link
        """
        return self._link_info.alttext

    @property
    def buildup_data(self):
        """
        Returns the LinkData objects for the link metadata
        """
        return self._link_info.buildup_data

    @property
    def is_plain(self):
        """
        Read only boolean. Returns true for links with no BuildUp meta data
        """
        return self.buildup_data is None

    @property
    def is_part(self):
        """
        Read only boolean. Returns true for links with BuildUp that describe
        part/tool usage.
        """
        if self.is_plain:
            return False
        return self.buildup_data.part

    @property
    def is_step(self):
        """
        Read only boolean. Returns true for links with BuildUp that describe
        another step in the documentation.
        """
        if self.is_plain:
            return False
        return self.buildup_data.step

    @property
    def is_output(self):
        """
        Read only boolean. Returns true for links with BuildUp that describe
        an part created on this page.
        """
        if self.is_plain:
            return False
        return self.buildup_data.output

    @property
    def is_bom(self):
        """
        Read only boolean. Returns true for links to bill of materials pages.
        """
        if self.is_plain:
            return False
        return self.buildup_data.bom

    @property
    def content_generated(self):
        """Returns true if the content is generated in build up and otherwise
        return false"""
        #Note the link_rel_to_page has converted library links into .md links
        if self.link_rel_to_page.endswith('.md'):
            return True
        if self.raw_linklocation.startswith('{{'):
            return True
        return False

    def as_output_file(self):
        """ Returns the link as an FileInfo object.
        If the link is to a buildup file `None` is returned as this is generated
        elsewhere.
        """
        if self.content_generated or self.location_undefined:
            return None
        return FileInfo(self.link_rel_to_root)

    def link_ref_md(self, url_translator):
        """
        Returns a plain markdown link reference for the link.
        Input is a URLTranslator object
        """
        location = self.output_url(url_translator)
        return f'[{self.linktext}]:{location} "{self.alttext}"'

    def link_md(self, url_translator, text_override=None):
        """
        Returns a plain markdown link for the link object, i.e. the part
        in the text not the reference.
        If this is a link reference object None is returned.
        Input is a URLTranslator object
        Optionally the link text can be overridden, this doesn't work for
        a reference style link as it would break it.
        """
        if self.is_output:
            anchor_name = clean_id(self.linktext)
            return f'<a name="output__{anchor_name}"></a>{self.linktext}'
        if self._link_type == self.LINK_REF:
            return None
        if self._link_type == self.IN_LINE_REF:
            return f'[{self.linktext}]'
        # A full inline link
        location = self.output_url(url_translator)
        if text_override is None:
            text = self.linktext
        else:
            text = text_override
        return f'[{text}]({location} "{self.alttext}")'

    def output_url(self, url_translator):
        """
        Uses url_translator a URLTranslator object
        to generate a link to the correct place.
        """
        return url_translator.translate(self)


class Link(BaseLink):
    '''
    A link to another file in the Documentation directory. See also LibraryLink
    and WebLink. This class should always be created with `make_link` which will
    create the correct link type. The child class Image can be created directly
    with its constructor.
    '''

    def __init__(self, link_info, page, link_type):
        super().__init__(link_info, page, link_type)
        if self._link_type == self.LINK_REF:
            if self._link_info.linklocation.lower() == "missing":
                self._link_info.linklocation = ''
                return

        if os.path.isabs(self._link_info.linklocation):
            _LOGGER.warning('Absolute path "%s" removed, only relative paths are supported.',
                            {self._link_info.linklocation})
            self._link_info.linklocation = ""
        if self.is_step and self._link_info.linklocation == '':
            _LOGGER.warning('A step link must link to a buildup page')
            self._link_info.buildup_data.step = False
        self._link_info.linklocation = self._link_info.linklocation

    @property
    def link_rel_to_root(self):
        """
        Location of the link relative to the root BuildUp directory
        """
        # Overloading to fix anchor only links
        location = self.link_rel_to_page
        if location.startswith('#'):
            return self._page+location
        return super().link_rel_to_root


class WebLink(BaseLink):
    """
    A child class of BaseLink for links to external webpages. Bypasses
    most of the link translation, etc
    """
    def __init__(self, link_info, page, link_type):
        super().__init__(link_info, page, link_type)
        if self.is_step:
            _LOGGER.warning('A step link must link to a buildup page')
            self._link_info.buildup_data.step = False

    @property
    def link_rel_to_page(self):
        """
        Returns just the url as it is a web link.
        """
        return self.raw_linklocation

    @property
    def link_rel_to_root(self):
        """
        Returns just the url as it is a web link.
        """
        return self.raw_linklocation

    def as_output_file(self):
        """
        Overload output file to None, as weblinks have no
        ouput file
        """
        return None

    def output_url(self, url_translator):
        """
        Overload output url to ignore translation
        """
        return self.raw_linklocation

    @property
    def content_generated(self):
        return False

class FromStepLink(BaseLink):
    """
    A child class of BaseLink for links to parts produced in previous documentation steps
    """
    def __init__(self, link_info, page, link_type):
        super().__init__(link_info, page, link_type)
        self._resolved = False
        if self.is_step:
            _LOGGER.warning('When linking to "FromStep" the link cannot be a step link')
            self._link_info.buildup_data.step = False

    def reset(self):
        """
        Resets the link to an unresoved state
        """
        self._resolved = False

    def resolve(self, outputs):
        """
        This function resolves the URL for a part defined in a previous step.
        Input is all of the outputs defined in prvious steps. Nothing is returned
        from this method. If the corresponing part is located FromStepLink.resolved
        will be set to True, if not a warning will be logged.
        """
        output_names = [link.linktext for link in outputs]
        if self.linktext in output_names:
            index = output_names.index(self.linktext)
            page_dir = os.path.dirname(self.page)
            self._link_info.linklocation = os.path.relpath(outputs[index].page, page_dir)
            self._resolved = True
        else:
            _LOGGER.warning('The step that defines [%s] cannot be found', self.linktext)

    @property
    def resolved(self):
        """
        Boolean property. Returns true if the step that defines the output has been
        resolved.
        """
        return self._resolved

    @property
    def link_rel_to_page(self):
        """
        Returns just the url as it is a web link.
        """
        if not self.resolved:
            return ""
        return super().link_rel_to_page


class LibraryLink(BaseLink):
    """
    A child class of BaseLink for links to parts in Libraries. It translates
    the from the link in the library to the final markdown page. Then other
    translations happen as standard.
    """

    def __init__(self, link_info, page, link_type, lib_match):
        super().__init__(link_info, page, link_type)
        if self.is_step:
            _LOGGER.warning('A step link must link to a buildup page')
            self._link_info.buildup_data.step = False
        libname = _fully_normalise_link(lib_match[1], page)
        #The id/key in the part library
        self._part_id = lib_match[2]
        self._output_rel_to_page = os.path.join(libname,
                                                self._part_id+'.md')
        page_dir = os.path.dirname(page)
        root_link = os.path.join(page_dir, lib_match[0])
        #This is the libray relative to the root
        self._library_file = os.path.normpath(root_link)


    @property
    def link_rel_to_page(self):
        """
        Location of the output part page relative to the BuildUp page
        """
        return self._output_rel_to_page

    @property
    def library_location(self):
        """
        Returns a tuple of the library file (relative to the root dir) and the
        part name.
        """
        return (self._library_file, self._part_id)

    @property
    def content_generated(self):
        """
        Always returns true as LibraryLinks always generate content
        """
        return True


class Image(Link):
    """
    A child class of Link to deal with the subtle differences of Links
    and Images in markdown.
    """

    def __init__(self, image_dict, page, link_references=None):

        image_dict["linktext"] = ''
        image_dict["buildup_data"] = None
        image_dict["linklocation"] = image_dict["imagelocation"]
        self._hovertext = image_dict["hovertext"]
        del image_dict["imagelocation"]
        del image_dict["hovertext"]
        link_info = LinkInfo(**image_dict)
        if link_info.linklocation == "":
            link_type = BaseLink.IN_LINE_REF
            link_info.linklocation = _complete_ref_style_link(link_info.linktext,
                                                              link_references)
        else:
            link_type = BaseLink.IN_LINE_FULL

        super().__init__(link_info,
                                    page=page,
                                    link_type=link_type)

    @property
    def image_rel_to_page(self):
        """
        Location of the image file relative to the BuildUp page
        """
        return self.link_rel_to_page

    @property
    def image_rel_to_root(self):
        """
        Location of the image file relative to the root BuildUp directory
        """
        return self.link_rel_to_root

    @property
    def hovertext(self):
        """
        Returns the hover text of the link
        """
        return self._hovertext

    def _library_match(self): # pylint: disable=no-self-use
        """
        This overrides the Link version of this functions and just
        returns false as an image cannot be a library.
        """
        return None

    def image_md(self, url_translator):
        """
        Returns a the plain markdown for the image
        """

        location = self.output_url(url_translator)
        return f'![{self.alttext}]({location} "{self.hovertext}")'

    def link_md(self, url_translator, _=None):
        """
        Redirects to `image_md`
        Perhaps warn if this is used?
        """
        return self.image_md(url_translator)
