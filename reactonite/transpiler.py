import os
from distutils.dir_util import copy_tree
from html.parser import HTMLParser

from bs4 import BeautifulSoup


class AttributesParser(HTMLParser):
    """Extends HTMLParser to extract tags with attributes from a given HTML string

    Call feed method of HTMLParser to generate data and then retriece it from
    the object of the class. Here's an usage example:

    attributes_parser = AttributesParser()
    attributes_parser.feed("YOUR_HTML_STRING")
    tag_with_attributes = attributes_parser.data
    print(tag_with_attributes)

    Attributes
    ----------
    data : list
        Stores the tags with their attributes
    """

    def handle_starttag(self, tag, attrs):
        """Overrides the original handler for start tag and appends the tags to data.

        Parameters
        ----------
        tag : str
            Name of tag being parsed
        attrs : list
            List of attrs corresponding to the current tag
        """

        attrDict = {}
        for attr in attrs:
            attrDict[attr[0]] = attr[1]
        try:
            self.data.append({
                tag: attrDict
            })
        except AttributeError:
            self.data = [{
                tag: attrDict
            }]


class ReactCodeMapper:
    """Class to convert tags and props from HTML to React

    Call getReactMap method for converting tags fed for HTML and get
    corresponding React Mapping. Here's an usage example:

    reactCodeMapper = ReactCodeMapper(destination_dir, props_map)
    react_map = reactCodeMapper.getReactMap(tag_with_attributes)
    print(react_map)

    Attributes
    ----------
    __IMAGE_TAG_HANDLER : str
        Stores handler corresponding to img tag
    __STYLE_TAG_HANDLER : str
        Stores handler corresponding to style tag
    __SCRIPT_TAG_HANDLER : str
        Stores handler corresponding to script tag
    __LINK_TAG_HANDLER : str
        Stores handler corresponding to link tag
    CUSTOM_TAG_HANDLERS : dict
        Stores mapping correspoding to tags which are handled seperately.
    dest_dir : str
        Destination directory for the React codebase.
    props_map : dict
        Mapping of attrs for HTML to React from props_map.py
    add_to_import : list
        Stores imports corresponding to variables created during transpilation.
    add_variables : list
        Stores newly created variables during transpilation.
    """

    __IMAGE_TAG_HANDLER = 'IMAGE_TAG_HANDLER'
    __STYLE_TAG_HANDLER = 'STYLE_TAG_HANDLER'
    __SCRIPT_TAG_HANDLER = 'SCRIPT_TAG_HANDLER'
    __LINK_TAG_HANDLER = 'LINK_TAG_HANDLER'

    CUSTOM_TAG_HANDLERS = {
        'img': __IMAGE_TAG_HANDLER,
        'style': __STYLE_TAG_HANDLER,
        'script': __SCRIPT_TAG_HANDLER,
        'link': __LINK_TAG_HANDLER
    }

    def __init__(self, dest_dir, props_map):
        self.dest_dir = dest_dir
        self.props_map = props_map
        self.add_to_import = []
        self.add_variables = []

    def __getSafeName(self, link):
        """Generates safe name for varibale from path to file.

        Parameters
        ----------
        link : str
            Path to file for which varibale is created.

        Returns
        -------
        str
            Variable name generated from link
        """

        varName = ""
        for ch in link:
            _ch = ch
            if not ch.isalnum():
                _ch = '_'
            varName += _ch
        return varName

    def __getLinkInfo(self, link):
        """Generates link information.

        If link is internal corresponding variable name is generated, for
        external link it is returned.

        Parameters
        ----------
        link : str
            Link for filepath or external link.

        Returns
        -------
        str
            Variable name generated from link or link in external case.
        """

        if os.path.exists(os.path.join(self.dest_dir, 'src', link)):
            var = self.__getSafeName(link)
            self.add_to_import.append(
                "import {var} from '{link}';".format(
                    var=var,
                    link=link
                )
            )
            self.add_variables.append(var)
            return "{" + var + "}"
        else:
            return link

    def __getAttrsWithLink(self, attrs, linkAttr):
        """Generates attrs for tags having links to other files.

        If link is internal corresponding variable name is generated, for
        external link it is returned.

        Parameters
        ----------
        attrs : dict
            Attributes of tag to be worked upon.
        linkAttr : str
            Name of attr that correspond to link of file, example 'src' in
            case of script tag

        Returns
        -------
        dict
            Final dictonary of attributes with link handled
        """

        final_attrs = {}
        for attrKey in attrs.keys():
            if attrKey == linkAttr:
                link_info = self.__getLinkInfo(attrs[attrKey])
                final_attrs['src'] = link_info
            else:
                final_attrs[attrKey] = attrs[attrKey]
        return final_attrs

    def __customTagAttrsHandler(self, attrs, tag_handler):
        """Custom tag and attributes handler for parsing attrs from CUSTOM_TAG_HANDLERS

        Parameters
        ----------
        attrs : dict
            Attributes for corresponding tag needed to be handled
        tag_handler : str
            Tag handler type to be used in mapping

        Returns
        -------
        dict
            Final attributes for that tag, if None is returned delete the tag
        """

        final_attrs = {}
        if tag_handler == self.__IMAGE_TAG_HANDLER:
            final_attrs = self.__getAttrsWithLink(attrs, 'src')
        elif tag_handler == self.__STYLE_TAG_HANDLER:
            print(attrs)
        elif tag_handler == self.__SCRIPT_TAG_HANDLER:
            if 'src' in attrs.keys():
                final_attrs = self.__getAttrsWithLink(attrs, 'src')
            else:
                return None
        elif tag_handler == self.__LINK_TAG_HANDLER:
            final_attrs = self.__getAttrsWithLink(attrs, 'href')
        return final_attrs

    def __getRenamedAttrs(self, attrs):
        """Generates renamed attributes correspoding to React.

        Parameters
        ----------
        attrs : dict
            Attributes in HTML format

        Returns
        -------
        dict
            Attributes in React format
        """

        final_attrs = {}
        for attrKey in attrs.keys():
            if attrKey in self.props_map:
                useKey = self.props_map[attrKey]
            else:
                useKey = attrKey
            final_attrs[useKey] = attrs[attrKey]
        return final_attrs

    def getReactMap(self, tags):
        """Wrapper to generate React Map object comprising of all data needed
        to convert HTML to React

        Parameters
        ----------
        tags : dict
            HTML attributes extracted using AttributesParser

        Returns
        -------
        dict
            Final mapping of tags with imports and varibles for React, if any
            attribute is None then tag needs to be deleted
        """

        final_map = {
            'imports': [],
            'tags': [],
            'variables': [],
        }
        for tag in tags:
            tag_name = list(tag.keys())[0]
            attrs = self.__getRenamedAttrs(tag[tag_name])
            if tag_name in self.CUSTOM_TAG_HANDLERS:
                attrs = self.__customTagAttrsHandler(
                    attrs,
                    self.CUSTOM_TAG_HANDLERS[tag_name]
                )
            final_map['tags'].append({tag_name: attrs})
        final_map['imports'] = "\n".join(self.add_to_import)
        final_map['variables'] = self.add_variables
        return final_map


class Transpiler:
    """Transpiler responsible for translating HTML code to React

    Attributes
    ----------
    src_dir : str
        Path of the source directory within the project directory
    dest_dir : str
        Path to the transpiled React app within the project directory
    parser : str, optional
        Specify which parser to use for reading HTML files, defaults
        to "html.parser"
    verbose : bool, optional
        Specify the verbosity of the transpiler, defaults to False
    """

    def __init__(self,
                 config_settings,
                 props_map,
                 verbose=False):
        """Transpiler initiator takes config settings and unpacks variables.

        Parameters
        ----------
        config_settings : dict
            Path to src_dir and dest_dir as dict object, stored in config.json
        props_map : dict
            Mapping of props for HTML to React used during transpilation
        verbose : bool, optional
            Specify the verbosity of the transpiler, deafults to False

        Raises
        ------
        RuntimeError
            Raised if the config_settings point to non existing dirs.
        """

        self.src_dir = config_settings["src_dir"]
        self.dest_dir = config_settings["dest_dir"]

        self.props_map = props_map

        if not os.path.exists(os.path.join(".", self.src_dir)):
            raise RuntimeError(
                "Source directory doesn't exist at " +
                str(self.src_dir)
            )

        if not os.path.exists(os.path.join(".", self.dest_dir)):
            raise RuntimeError(
                "Destination directory doesn't exist at " +
                str(self.dest_dir)
            )

        self.parser = "html.parser"
        self.verbose = verbose

    def __replaceAttrs(self, soup, tag_name, or_attrs, f_attrs):
        """Replaces the attrs for updated tags comparing original and final attrs.

        Parameters
        ----------
        soup : BeautifulSoup
            bs4.BeautifulSoup passed by reference.
        tag_name : str
            Name of tag being worked upon.
        or_attrs : dict
            Dictonary consisting of original attributes of HTML.
        f_attrs : dict
            Dictonary consisting of final attributes for React.
        """

        if or_attrs == f_attrs:
            return
        soup.find(tag_name, attrs=or_attrs).attrs = f_attrs

    def __deleteTag(self, soup, tag_name, attrs):
        """Deletes the tag corresponding to given tag_name and attrs.

        Parameters
        ----------
        soup : BeautifulSoup
            bs4.BeautifulSoup passed by reference.
        tag_name : str
            Name of tag being worked upon.
        attrs : dict
            Dictonary consisting of original attributes of HTML.
        """

        soup.find(tag_name, attrs=attrs).decompose()

    def __generateReactFileContent(self, soup, function_name):
        """Generates React code from HTML soup object.

        Parameters
        ----------
        soup : BeautifulSoup
            bs4.BeautifulSoup with HTML code to be transpiled.
        function_name : str
            Function name to be used from filename without extension.

        Returns
        -------
        str
            Content for React file.
        """

        attributes_parser = AttributesParser()
        attributes_parser.feed(soup.prettify())
        tag_with_attributes = attributes_parser.data

        reactCodeMapper = ReactCodeMapper(self.dest_dir, self.props_map)
        react_map = reactCodeMapper.getReactMap(tag_with_attributes)

        final_tags = react_map['tags']
        react_variables = react_map['variables']

        for orignal_tag, fianl_tag in zip(tag_with_attributes, final_tags):
            or_tag_name = list(orignal_tag.keys())[0]
            or_attrs = orignal_tag[or_tag_name]
            f_tag_name = list(fianl_tag.keys())[0]
            f_attrs = fianl_tag[f_tag_name]

            if or_tag_name == f_tag_name:
                if f_attrs is None:
                    self.__deleteTag(soup, or_tag_name, or_attrs)
                else:
                    self.__replaceAttrs(soup, or_tag_name, or_attrs, f_attrs)
            else:
                raise RuntimeWarning(
                    "There's an error in processing " +
                    or_tag_name
                )

        soup.head.name = 'Helmet'

        body_contents = [
            x.encode('utf-8').decode("utf-8") for x in soup.body.contents[1:-1]
        ]
        body_str = "".join(body_contents)

        content_str = soup.Helmet.prettify() + body_str

        for variable in react_variables:
            content_str = content_str.replace(
                '"{' + variable + '}"',
                '{' + variable + '}'
            )

        react_function = "function " + function_name + "() {return (<>" + \
            content_str + "</>);}"

        return """
        import React from 'react';
        import Helmet from 'react-helmet';
        {imports}

        {function}

        export default App;
        """.format(function=react_function, imports=react_map['imports'])

    def __copyStaticFolderToDest(self):
        """Copies source static folder to the transpiled React code static
        folder inside src
        """

        static_src_dir = os.path.join(self.src_dir, "static")
        static_dest_dir = os.path.join(self.dest_dir, "src", "static")

        if not os.path.exists(static_src_dir):
            return

        if self.verbose:
            print('Copying static folder directory...')

        copy_tree(static_src_dir, static_dest_dir)

    def __transpileFile(self, filepath, is_init_html=False):
        """Transpiles the source HTML file given at the given filepath
        to a React code, which is then copied over to the React build
        directory

        Parameters
        ----------
        filepath : str
            Path to the source HTML file which is to be transpiled
        is_init_html : bool, optional
            Set to True if file to be transpiled is init html file as it will
            be renamed to App.js

        Raises
        ------
        RuntimeError
            Raised if the source html file doesn't have a .html
            extention
        """

        _, filename = os.path.split(filepath)
        filenameWithNoExtension, file_extension = os.path.splitext(filename)

        if file_extension != ".html":
            raise RuntimeError(str(filename) + ' is not a HTML file')

        if is_init_html:
            filenameWithNoExtension = "App"

        filename = filenameWithNoExtension + ".js"

        dest_filepath = os.path.join(self.dest_dir, 'src', filename)

        if self.verbose:
            print(
                "Transpiling file " + str(filepath) +
                " -> " + str(dest_filepath)
            )

        with open(filepath, 'r') as index:
            soup = BeautifulSoup(index, self.parser)

        with open(dest_filepath, 'w') as outfile:
            file_content = self.__generateReactFileContent(
                soup,
                filenameWithNoExtension
            )
            outfile.write(file_content)

    def transpile_project(self):
        """Runs initial checks like ensuring the source
        directories exist, and the source file is present.
        After that, copies static files and transpiles the source.

        Raises
        ------
        RuntimeError
            Raised source html file is missing.
        """

        entry_point_html = os.path.join(self.src_dir, 'index.html')

        if not os.path.isfile(entry_point_html):
            raise RuntimeError(
                "Entry point file doesn't exist at " +
                str(entry_point_html)
            )

        # Copy static assests
        self.__copyStaticFolderToDest()

        if self.verbose:
            print("Transpiling files...")

        # TODO: Next Release, Loop through all files/dirs in src folder except
        self.__transpileFile(
            entry_point_html,
            is_init_html=True
        )
