"""
This submodule handles buildup part libraries. It parses the contents of the library
files, identifies parts in the libraries, and generates markdown pages for parts.
"""

import os
import regex as re
import logging
import yaml
from gitbuilding.buildup.files import FileInfo

_LOGGER = logging.getLogger('BuildUp')

def _write_part_markdown(part_name, part_info):
    """
    Generates the markdown for a part from a part library
    """

    if "Name" in part_info:
        md = f'# {part_info["Name"]}\n\n'
    else:
        md = f"# {part_name}\n\n"

    if "Description" in part_info:
        md += f'{part_info["Description"]}\n\n'
    if "Specs" in part_info:
        md += _write_specs_markdown(part_info["Specs"])
    if "Suppliers" in part_info:
        md += _write_supplier_markdown(part_info["Suppliers"])
    return md

def _write_specs_markdown(part_specs):
    """
    Generates the markdown for the specifications for part from a part library
    """
    if isinstance(part_specs, dict):
        md = "\n\n## Specifications\n\n|Attribute |Value|\n|---|---|\n"
        for skey in part_specs:
            md += f'|{skey}|{part_specs[skey]:}|\n'
        return md
    _LOGGER.warning("Invalid specifications in Part Library, skipping.")
    return ""

def _write_supplier_markdown(suppliers):
    """
    Generates the markdown for the suppliers of a part from a part library
    """
    if isinstance(suppliers, dict):
        md = "\n\n## Suppliers\n\n|Supplier |Part Number|\n|---|---|\n"
        for skey in suppliers:
            if "Link" in suppliers[skey]:
                link = suppliers[skey]["Link"]
            else:
                link = "missing"
            if "PartNo" in suppliers[skey]:
                part_no = suppliers[skey]["PartNo"]
            else:
                part_no = "Unknown"
            md += f"|{skey}|[{part_no}]({link})|\n"
        return md
    _LOGGER.warning("Invalid supplier list in Part Library, skipping.")
    return ""


class Libraries:
    """
    Class to handle all the part libraries for the documentation. This object is
    initialised with the file main documentation filelist. Libraries are not parsed
    until the first time they are used. Any YAML file is assumed to be a library
    any non-yaml file is not a library.
    This should be modified to have a defined schema to check which YAML files are
    part libraries. Also other files formats that support this schema should be
    added (JSON, TOML, XML, etc). CSV support will also be added, need a way to convert
    between CSV and the nested dictionary structure of the schema.
    """

    def __init__(self, filelist):
        self._libraries = []
        self._filelist = filelist

    @property
    def library_names(self):
        """
        This is a property to give a lists of just the library names (filename)
        Calling in repeatedly is inefficient as it builds them each time
        """
        return [lib["name"] for lib in self._libraries]

    def get_library(self, library, add_missing=False):
        """
        Returns the library dictionary structure of the named library
        """

        if not self.listed(library):
            if not add_missing:
                return None
            added = self.add_library(library)
            if not added:
                # if library couldn't be added we return. Warning generated by
                # add_library
                return None
        return self._libraries[self.library_names.index(library)]["lib"]

    def listed(self, library):
        """
        Checks if there is a library named <library> in the list of
        libraries. Note library names are the input file name
        """
        return library in self.library_names

    def add_library(self, library_filename):
        """
        Adds the contents of library_filename to the library list if it is not already in there.
        The library dictionary is identified by the file name
        """
        if self.listed(library_filename):
            return False

        if library_filename not in self._filelist:
            _LOGGER.warning("Cannot find library '%s'", library_filename)
            return False

        library_file = self._filelist[self._filelist.index(library_filename)]
        if not library_file.dynamic_content:
            _LOGGER.warning("Cannot read library '%s'", library_filename)
            return False

        try:
            partslib = yaml.load(library_file.content, Loader=yaml.SafeLoader)
        except yaml.error.YAMLError:
            _LOGGER.warning("'%s' is invalid YAML", library_filename)
            return False

        self._libraries.append({"name": library_filename,
                                "lib": partslib})
        return True

    def part_md(self, library, part_name):
        """
        Returns the markown for a part in a part library
        """
        part_lib = self.get_library(library, add_missing=True)
        if part_lib is not None and part_name in part_lib:
            part_info = part_lib[part_name]
            md = _write_part_markdown(part_name, part_info)
            return md
        _LOGGER.warning('Part %s is not in library %s', part_name, library)
        return None

    def part_page(self, library, part_name):
        """
        This function makes a markdown page for a part in a library.
        """
        md = self.part_md(library, part_name)
        if md is None:
            return None
        libdir = re.match(r"^(.+)\.ya?ml$", library).group(1)
        filepath = os.path.join(libdir, f"{part_name}.md")
        return FileInfo(filepath,
                        dynamic_content=True,
                        content=md)
