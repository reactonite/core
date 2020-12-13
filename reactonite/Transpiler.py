import glob
import os
from distutils.file_util import copy_file
from html.parser import HTMLParser

from bs4 import BeautifulSoup, Comment

from .NodeWrapper import NodeWrapper


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

    reactCodeMapper = ReactCodeMapper(source_dir, destination_dir, props_map)
    react_map = reactCodeMapper.getReactMap(tag_with_attributes)
    print(react_map)

    Attributes
    ----------
    CUSTOM_TAG_HANDLERS : dict
        Stores mapping correspoding to tags which are handled seperately.
    src_dir : str
        Source directory for the HTML codebase.
    dest_dir : str
        Destination directory for the React codebase.
    props_map : dict
        Mapping of attrs for HTML to React from props_map.py
    add_to_import : list
        Stores imports corresponding to variables created during transpilation.
    add_variables : list
        Stores newly created variables during transpilation.
    router_link_imported : bool, optional
        Saves wether Link tag needs to be imported for current page.
    """

    def __init__(self, src_dir, dest_dir, props_map):
        self.src_dir = src_dir
        self.dest_dir = dest_dir
        self.props_map = props_map
        self.add_to_import = []
        self.add_variables = []
        self.router_link_imported = False

        self.__A_TAG_HANDLER = 'A_TAG_HANDLER'
        self.__IMAGE_TAG_HANDLER = 'IMAGE_TAG_HANDLER'
        self.__SCRIPT_TAG_HANDLER = 'SCRIPT_TAG_HANDLER'
        self.__STYLE_TAG_HANDLER = "STYLE_TAG_HANDLER"
        self.__LINK_TAG_HANDLER = 'LINK_TAG_HANDLER'

        self.CUSTOM_TAG_HANDLERS = {
            'a': self.__A_TAG_HANDLER,
            'img': self.__IMAGE_TAG_HANDLER,
            'script': self.__SCRIPT_TAG_HANDLER,
            'style': self.__STYLE_TAG_HANDLER,
            'link': self.__LINK_TAG_HANDLER
        }

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

    def __getLinkInfo(self, link, filepath_from_src, no_var=False):
        """Generates link information.

        If link is internal corresponding variable name is generated, for
        external link it is returned.

        Parameters
        ----------
        link : str
            Link for filepath or external link.
        filepath_from_src : str
            Path to file from src.
        no_var : bool, optional
            To generate import variable or just import file, default is False
            i.e. generate variable

        Returns
        -------
        str
            Variable name generated from link or link in external case.
        """

        if link:
            pathToLink = os.path.join(self.src_dir, filepath_from_src, link)
            pathToIndexLink = os.path.join(pathToLink, 'index.html')
            if os.path.isfile(pathToLink) or os.path.isfile(pathToIndexLink):
                var = self.__getSafeName(link)
                if no_var:
                    self.add_to_import.append(
                        "import '{link}';".format(
                            link=link
                        )
                    )
                    return None
                else:
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

    def __getAttrsWithLink(
        self, attrs, linkAttr, filepath_from_src, no_var=False
    ):
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
        filepath_from_src : str
            Path to file from src directory.
        no_var : bool, optional
            To generate import variable or just import file, default is False
            i.e. generate variable

        Returns
        -------
        dict
            Final dictonary of attributes with link handled
        """

        final_attrs = {}
        for attrKey in attrs.keys():
            if attrKey == linkAttr:
                link_info = self.__getLinkInfo(
                    attrs[attrKey],
                    filepath_from_src,
                    no_var=no_var
                )
                if link_info is None:
                    return None
                final_attrs[linkAttr] = link_info
            else:
                final_attrs[attrKey] = attrs[attrKey]
        return final_attrs

    def __getAttrsForRouterLink(
        self, attrs, filepath_from_src
    ):
        """Generates attrs for A tag having links to other files.

        If link is internal that is checked and also link is generated is
        generated, for external link it is returned.

        Parameters
        ----------
        attrs : dict
            Attributes of tag to be worked upon.
        filepath_from_src : str
            Path to file from src directory.

        Returns
        -------
        tuple
            Tuple of final dictonary of attributes with link handled and
            information about internal link
        """

        final_attrs = {}
        is_internal = False
        for attrKey in attrs.keys():
            if attrKey == "href":
                href_info = attrs[attrKey]
                pathRef = os.path.join(
                    self.src_dir, filepath_from_src, href_info
                )
                pathRefIndex = os.path.join(
                    self.src_dir, filepath_from_src, href_info, "index.html"
                )
                if os.path.isfile(pathRef) or os.path.isfile(pathRefIndex):
                    htmlPath = os.path.normpath(
                        os.path.join(filepath_from_src, href_info)
                    )
                    jsPath = '/'.join(htmlPath.split(os.path.sep))
                    jsPath = jsPath.replace(".html", "")
                    if jsPath == "index":
                        jsPath = "/"
                    is_internal = True
                    final_attrs["to"] = jsPath
                else:
                    final_attrs["href"] = href_info
            else:
                final_attrs[attrKey] = attrs[attrKey]
        return final_attrs, is_internal

    def __customTagAttrsHandler(self, attrs, tag_handler, filepath_from_src):
        """Custom tag and attributes handler for parsing attrs from CUSTOM_TAG_HANDLERS

        Parameters
        ----------
        attrs : dict
            Attributes for corresponding tag needed to be handled
        tag_handler : str
            Tag handler type to be used in mapping
        filepath_from_src : str
            Path to file from src directory

        Returns
        -------
        dict
            Final attributes for that tag, if None is returned delete the tag
        """

        final_attrs = {}
        if tag_handler == self.__A_TAG_HANDLER:
            final_attrs, is_internal_link = self.__getAttrsForRouterLink(
                attrs, filepath_from_src
            )
            if not self.router_link_imported and is_internal_link:
                self.add_to_import.append(
                    'import {Link} from "react-router-dom";'
                )
                self.router_link_imported = True
        elif tag_handler == self.__IMAGE_TAG_HANDLER:
            final_attrs = self.__getAttrsWithLink(
                attrs, 'src', filepath_from_src
            )
        elif tag_handler == self.__SCRIPT_TAG_HANDLER:
            if 'src' in attrs.keys():
                final_attrs = self.__getAttrsWithLink(
                    attrs, 'src', filepath_from_src
                )
            else:
                return None
        elif tag_handler == self.__STYLE_TAG_HANDLER:
            return None
        elif tag_handler == self.__LINK_TAG_HANDLER:
            # css variable was added delete other link tags
            if attrs["rel"] == "stylesheet":
                final_attrs = self.__getAttrsWithLink(
                        attrs,
                        'href',
                        filepath_from_src,
                        no_var=True
                    )
            return None
        return final_attrs

    def __getReactAttrs(self, attrs):
        """Generates renamed attributes correspoding to React, and removes
        inline style tags and tags starting with on like onclick etc.

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
            if attrKey == "style":
                continue
            if attrKey.startswith("on"):
                continue
            if attrKey in self.props_map:
                useKey = self.props_map[attrKey]
            else:
                useKey = attrKey
            final_attrs[useKey] = attrs[attrKey]
        return final_attrs

    def getReactMap(self, tags, filepath_from_src):
        """Wrapper to generate React Map object comprising of all data needed
        to convert HTML to React

        Parameters
        ----------
        tags : dict
            HTML attributes extracted using AttributesParser
        filepath_from_src : str
            Path to file from src directory

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
            attrs = self.__getReactAttrs(tag[tag_name])
            if tag_name in self.CUSTOM_TAG_HANDLERS:
                attrs = self.__customTagAttrsHandler(
                    attrs,
                    self.CUSTOM_TAG_HANDLERS[tag_name],
                    filepath_from_src
                )
            final_map['tags'].append({tag_name: attrs})
        final_map['imports'] = "\n".join(self.add_to_import)
        final_map['variables'] = self.add_variables
        return final_map


class Transpiler:
    """Transpiler responsible for translating HTML code to React

    Attributes
    ----------
    project_name : str
        Name of the project as stored in config
    src_dir : str
        Path of the source directory within the project directory
    dest_dir : str
        Path to the transpiled React app within the project directory
    index_routes : dict
        Stores Routes data corresponding to different pages for index.js
    parser : str, optional
        Specify which parser to use for reading HTML files, defaults
        to "html.parser"
    verbose : bool, optional
        Specify the verbosity of the transpiler, defaults to False
    """

    def __init__(self,
                 config_settings,
                 props_map,
                 verbose=False,
                 create_project=False):
        """Transpiler initiator takes config settings and unpacks variables.

        Parameters
        ----------
        config_settings : dict
            project_name, src_dir, dest_dir as dict object stored
            in config.json
        props_map : dict
            Mapping of props for HTML to React used during transpilation
        verbose : bool, optional
            Specify the verbosity of the transpiler, deafults to False
        create_project : bool, optional
            Set to True if create project is calling method, deafults to False

        Raises
        ------
        RuntimeError
            Raised if the config_settings point to non existing dirs.
        """

        self.project_name = config_settings["project_name"]
        self.src_dir = config_settings["src_dir"]
        self.dest_dir = config_settings["dest_dir"]
        self.props_map = props_map
        self.index_routes = {}
        self.parser = "html.parser"
        self.verbose = verbose

        if create_project:
            self.src_dir = os.path.join('.', self.project_name, self.src_dir)
            self.dest_dir = os.path.join('.', self.project_name, self.dest_dir)

        npm = NodeWrapper()

        if not os.path.exists(os.path.join(".", self.src_dir)):
            raise RuntimeError(
                "Source directory doesn't exist at " +
                str(self.src_dir)
            )

        if not os.path.exists(os.path.join(".", self.dest_dir)):
            if create_project:
                project_dir = os.path.join(".", self.project_name)
                npm.create_react_app(
                    project_name=self.project_name,
                    working_dir=project_dir,
                    rename_to=self.dest_dir
                )
            else:
                npm.create_react_app(
                    project_name=self.project_name,
                    rename_to=self.dest_dir
                )

            # Install NPM packages
            npm.install(package_name='react-helmet', working_dir=self.dest_dir)
            npm.install(
                package_name='react-router-dom',
                working_dir=self.dest_dir
            )

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

        htmlTag = soup.find(tag_name, attrs=or_attrs)

        upperAttrs = {}
        lowerAttrs = {}

        if htmlTag is None:
            for attr in or_attrs.keys():
                upperAttrs[attr] = or_attrs[attr].upper()
                lowerAttrs[attr] = or_attrs[attr].lower()
            htmlTag = soup.find(tag_name, attrs=upperAttrs)
            if htmlTag is None:
                htmlTag = soup.find(tag_name, attrs=lowerAttrs)

        if not (htmlTag is None):
            htmlTag.attrs = f_attrs
            if tag_name == "a" and "to" in f_attrs:
                htmlTag.name = "Link"

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

        htmlTag = soup.find(tag_name, attrs=attrs)

        upperAttrs = {}
        lowerAttrs = {}
        if htmlTag is None:
            for attr in attrs.keys():
                upperAttrs[attr] = attrs[attr].upper()
                lowerAttrs[attr] = attrs[attr].lower()
            htmlTag = soup.find(tag_name, attrs=upperAttrs)
            if htmlTag is None:
                htmlTag = soup.find(tag_name, attrs=lowerAttrs)
        if not (htmlTag is None):
            htmlTag.decompose()

    def __generateReactFileContent(
        self, soup, function_name, filepath_from_src
    ):
        """Generates React code from HTML soup object.

        Parameters
        ----------
        soup : BeautifulSoup
            bs4.BeautifulSoup with HTML code to be transpiled.
        function_name : str
            Function name to be used from filename without extension with
            first letter capitalized
        filepath_from_src : str
            Path to file from src directory

        Returns
        -------
        str
            Content for React file.
        """

        styleTags = [style.extract() for style in soup.find_all('style')]
        scriptTags = [
            script.extract() for script in soup.find_all('script', src=False)
        ]
        attributes_parser = AttributesParser()
        attributes_parser.feed(soup.prettify())
        tag_with_attributes = attributes_parser.data

        reactCodeMapper = ReactCodeMapper(
            self.src_dir, self.dest_dir, self.props_map
        )
        react_map = reactCodeMapper.getReactMap(
            tag_with_attributes, filepath_from_src
        )

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

        reactHead = None
        if soup.head:
            soup.head.name = 'Helmet'
            reactHead = soup.Helmet
        else:
            if len(styleTags):
                reactHead = soup.new_tag('Helmet')

        if len(styleTags):
            for style in styleTags:
                reactHead.append(style)

        contents = soup.body.contents

        body_contents = [
            x.encode('utf-8').decode("utf-8").strip() for x in contents
        ]
        body_str = "".join(body_contents)

        if reactHead:
            content_str = reactHead.prettify() + body_str
            react_map['imports'] += "import Helmet from 'react-helmet';"
        else:
            content_str = body_str

        for variable in react_variables:
            content_str = content_str.replace(
                '"{' + variable + '}"',
                '{' + variable + '}'
            )

        if len(scriptTags):
            react_map['imports'] += "import React, { useEffect } from 'react';"
            scriptContent = ""
            for script in scriptTags:
                scriptContent += "".join(script.contents)
            useEffect = "useEffect(() => {" + scriptContent + "}, []);"
        else:
            react_map['imports'] += "import React from 'react';"
            useEffect = ""

        if len(styleTags):
            content_str = content_str.replace("<style>", "<style>{`")
            content_str = content_str.replace("</style>", "`}</style>")

        react_function = "function " + function_name + "() {  " + useEffect + \
            "  return (<>" + content_str + "</>);}"

        return """
        {imports}

        {function}

        export default {function_name};
        """.format(
            function_name=function_name,
            function=react_function,
            imports=react_map['imports']
        )

    def __getReactComponentName(self, link):
        """Generates safe name for React compnents from path to file.

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
        return "REACTONITE" + varName.upper()

    def __generateIndexJsContent(self):
        """Generates content for index.js file in React codebase with handled routes

        Returns
        -------
        str
            Content for index.js file in React codebase
        """

        router = """import {
                        BrowserRouter as Router,
                        Switch,
                        Route
                    } from "react-router-dom";"""

        imports = []
        routes = []

        for link, path in self.index_routes.items():
            componentName = self.__getReactComponentName(path)
            importReact = 'import ' + componentName + ' from "' + path + '";'
            imports.append(importReact)
            routeReact = """
            <Route path="/{link}">
                <{componentName} />
            </Route>
            """.format(link=link, componentName=componentName)
            routes.append(routeReact)

        imports = '\n'.join(imports)
        routes = '\n'.join(routes)

        return """
        import React from "react";
        import ReactDOM from "react-dom";
        import * as serviceWorkerRegistration from \
            "./serviceWorkerRegistration";
        import reportWebVitals from "./reportWebVitals";
        {router}

        import App from "./App";
        {imports}

        ReactDOM.render(
        <Router>
            <Switch>
            {routes}
            <Route path="/">
                <App />
            </Route>
            </Switch>
        </Router>,
        document.getElementById("root")
        );

        // If you don't want your app to work offline, you can change
        // register() to unregister() below. Note this comes with some
        // pitfalls. Learn more about service workers: https://cra.link/PWA
        serviceWorkerRegistration.register();

        // If you want to start measuring performance in your app, pass a
        // function to log results (for example: reportWebVitals(console.log))
        // or send to analytics endpoint. Learn more: https://bit.ly/CRA-vitals
        reportWebVitals();
        """.format(imports=imports, routes=routes, router=router)

    def __rebuildIndexJs(self):
        """Generates the index.js for React apps entry point, needed to handle
        links to pages

        Raises
        ------
        RuntimeError
            Raised if the index.js file is not found in dest_dir
        """

        pathToIndexJs = os.path.join(self.dest_dir, 'src', 'index.js')
        if not os.path.isfile(pathToIndexJs):
            raise RuntimeError("Looks like you are missing index.js file in \
                React directory! It seems to be an NPM/React issue rather.")

        with open(pathToIndexJs, 'w') as outfile:
            file_content = self.__generateIndexJsContent()
            outfile.write(file_content)

        NodeWrapper().prettify(path=pathToIndexJs)

    def __addRoutesToIndexLinkArray(self, filePathFromSrc, filenameNoExt):
        """Adds links to self.index_routes to be used in index.js generation

        Parameters
        ----------
        filePathFromSrc : str
            Path to the folder where file is in dest_dir folder from src
        filenameNoExt : str
            Filename with no extension
        """

        if filenameNoExt == "index":
            htmlPath = os.path.normpath(filePathFromSrc)
            jsPath = '/'.join(htmlPath.split(os.path.sep))
            self.index_routes[jsPath] = "./" + jsPath + "/index"
        else:
            htmlPath = os.path.normpath(os.path.join(
                filePathFromSrc, filenameNoExt
            ))
            jsPath = '/'.join(htmlPath.split(os.path.sep))
            self.index_routes[jsPath] = "./" + jsPath

    def transpileFile(self, filepath):
        """Transpiles the source HTML file given at the given filepath
        to a React code, which is then copied over to the React build
        directory, if not HTML file then get's copied directly.

        Parameters
        ----------
        filepath : str
            Path to the source HTML file which is to be transpiled

        Raises
        ------
        RuntimeError
            Raised if the source html file is not found
        """

        filePathFromSrc, _ = os.path.split(filepath[filepath.find('src') + 4:])
        _, filename = os.path.split(filepath)
        filenameWithNoExtension, file_extension = os.path.splitext(filename)

        if file_extension != ".html":
            dest_filepath = os.path.join(
                self.dest_dir, 'src', filePathFromSrc, filename
            )
            if self.verbose:
                print(
                    "Copying file " + str(filepath) +
                    " -> " + str(dest_filepath)
                )
            os.makedirs(os.path.dirname(dest_filepath), exist_ok=True)
            copy_file(filepath, dest_filepath)
            return

        if not os.path.isfile(filepath):
            raise RuntimeError("{} file not found".format(filepath))

        is_entry_point = False
        entry_point_html = os.path.join(self.src_dir, 'index.html')

        if entry_point_html == filepath:
            is_entry_point = True
            filenameWithNoExtension = "App"

        filename = filenameWithNoExtension + ".js"

        if not os.path.isdir(os.path.join(self.dest_dir, 'src')):
            raise RuntimeError("Looks like your React project didn't get \
                created please check your " + self.dest_dir + " for a src \
                    folder")

        dest_filepath = os.path.join(
            self.dest_dir, 'src', filePathFromSrc, filename
        )

        if self.verbose:
            print(
                "Transpiling file " + str(filepath) +
                " -> " + str(dest_filepath)
            )

        with open(filepath, 'r') as index:
            soup = BeautifulSoup(index, self.parser)

        # Remove all comments
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        [comment.extract() for comment in comments]

        os.makedirs(os.path.dirname(dest_filepath), exist_ok=True)
        with open(dest_filepath, 'w') as outfile:
            file_content = self.__generateReactFileContent(
                soup,
                filenameWithNoExtension.capitalize(),
                filePathFromSrc
            )
            outfile.write(file_content)

        NodeWrapper().prettify(path=dest_filepath)

        if not is_entry_point:
            self.__addRoutesToIndexLinkArray(
                filePathFromSrc, filenameWithNoExtension
            )

    def transpile_project(self):
        """Runs initial checks like ensuring the source
        directories exist, and the source file is present.
        After that, copies non html files and transpiles the source.

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

        if self.verbose:
            print("Transpiling files...")

        for filename in glob.iglob(self.src_dir + '**/**', recursive=True):
            if os.path.isfile(filename):
                self.transpileFile(
                    filename
                )

        self.__rebuildIndexJs()
