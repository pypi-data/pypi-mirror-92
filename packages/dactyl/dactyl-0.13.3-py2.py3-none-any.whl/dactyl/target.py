################################################################################
## Dactyl Target Class
##
## Defines a group of pages that are built together.
################################################################################

from dactyl.common import *
from dactyl.config import DactylConfig
from dactyl.openapi import ApiDef
from dactyl.page import DactylPage

class DactylTarget:
    def __init__(self, config, name=None, inpages=None, spec_path=None):
        assert isinstance(config, DactylConfig)
        self.config = config
        self.pages = None
        self.cover = None

        # Set self.data based on the input type
        if inpages is not None:
            self.from_adhoc(inpages)
        elif spec_path is not None:
            self.from_openapi(spec_path)
        else:
            self.from_config(name)
        self.name = self.data["name"]

        # Load *ALL* pages in config, in case some of them need to be referenced
        # by pages in this target
        self.config.load_pages()


    def from_config(self, name=None):
        """
        Pick a target from the existing config file, by its short name.
        If no name is provided, use whichever target is listed first.
        """
        if name is None:
            if len(self.config["targets"]) == 0:
                logger.critical("No targets found. Either specify a config file or --pages")
                exit(1)
            self.data = self.config["targets"][0]
        else:
            try:
                self.data = next(t for t in self.config["targets"] if t["name"] == name)
            except StopIteration:
                logger.critical("Unknown target: %s" % name)
                exit(1)

    def from_adhoc(self, inpages):
        """
        Create an ad-hoc target from a list of input pages, generally passed as
        a list of files from the commandline.
        """
        t = {
            "name": ADHOC_TARGET,
            "display_name": UNTITLED_TARGET,
        }

        # if len(inpages) == 1:
        #     t["display_name"] = guess_title_from_md_file(inpages[0])

        for inpage in inpages:
            # Figure out the actual filename and location of this infile
            # and set the content source dir appropriately
            in_dir, in_file = os.path.split(inpage)
            self.config["content_path"] = in_dir

            # Figure out what html file to output to
            ENDS_IN_MD = re.compile("\.md$", re.I)
            if re.search(ENDS_IN_MD, in_file):
                out_html_file = re.sub(ENDS_IN_MD, ".html", in_file)
            else:
                out_html_file = in_file+".html"

            new_page = {
                "md": in_file,
                "html": out_html_file,
                "targets": [ADHOC_TARGET],
                "category": "Pages",
                "pp_dir": in_dir,
            }
            self.config["pages"].append(new_page)

        self.data = t
        self.config["targets"].append(t)

    def from_openapi(self, spec_path):
        """
        Create a target from an API spec path.
        """

        openapi = ApiDef.from_path(spec_path)
        t = {
            "name": openapi.api_slug,
            "display_name": openapi.api_title,
        }

        self.config["pages"] = [{
            "openapi_specification": spec_path,
            "api_slug": openapi.api_slug,
            "targets": [openapi.api_slug],
        }]
        self.data = t
        openapi.add_metadata(self.data)
        self.config["targets"].append(t)

    def slug_name(self, fields_to_use=[], separator="-"):
        """Make a name for the target that's safe for use in URLs & filenames,
        from human-readable fields"""
        filename_segments = []
        for fieldname in fields_to_use:
            if fieldname in self.data.keys():
                filename_segments.append(slugify(self.data[fieldname]))

        if filename_segments:
            return separator.join(filename_segments)
        else:
            return slugify(self.name)

    def es_index_name(self):
        return self.slug_name(self.config["es_index_fields"],
                              self.config["es_index_separator"])

    def add_cover(self):
        """
        Instantiate the default cover page so self.load_pages() can include it.
        """
        coverpage_data = self.config["cover_page"]
        coverpage_data["targets"] = [self.name]
        skip_pp = self.config.get("skip_preprocessor", False)
        more_filters = self.data.get("filters", [])
        self.cover = DactylPage(self.config, coverpage_data, skip_pp, more_filters)

    def default_pdf_name(self):
        """Choose a reasonable name for a PDF file in case one isn't specified."""
        return self.slug_name(self.config["pdf_filename_fields"],
                              self.config["pdf_filename_separator"]) + ".pdf"


    def should_include(self, page):
        """Report whether a given page should be part of this target"""
        if "targets" not in page:
            return False
        if self.name in page["targets"]:
            return True
        else:
            return False

    def gain_fields(self, fields):
        """
        Add the provided fields to this target's definition
        """
        merge_dicts(fields, self.data, RESERVED_KEYS_TARGET, override=True)


    def expand_openapi_spec(self, page_data):
        """Expand OpenAPI Spec placeholders into a full page list"""
        assert OPENAPI_SPEC_KEY in page_data.keys()

        logger.debug("Expanding OpenAPI spec from placeholder: %s"%page_data)
        api_slug = page_data.get(API_SLUG_KEY, None)
        extra_fields = {}
        merge_dicts(self.data, extra_fields, RESERVED_KEYS_TARGET)
        merge_dicts(page_data, extra_fields, [OPENAPI_SPEC_KEY, API_SLUG_KEY])

        template_path = page_data.get(OPENAPI_TEMPLATE_PATH_KEY, None)
        swagger = ApiDef.from_path(page_data[OPENAPI_SPEC_KEY], api_slug,
                                       extra_fields, template_path)
        skip_pp = self.config.get("skip_preprocessor", False)
        made_pages = []
        for p in swagger.create_pagelist():
            more_filters = self.data.get("filters", [])
            po = DactylPage(self.config, p, skip_pp, more_filters)
            # Special case for filters; concatenate filter lists,
            # with target's filters first.
            if "filters" in self.data:
                po.gain_filters(self.data["filters"])
            made_pages.append(po)
        return made_pages

    def load_pages(self):
        """
        Find the set of pages that this target should include.  At this time,
        we expand OpenAPI spec placeholders into individual pages, read
        frontmatter, and so on. Save it to self.pages for later reference.
        """
        pages = []
        if self.cover:
            merge_dicts(self.data, self.cover.data, RESERVED_KEYS_TARGET)
            pages.append(self.cover)
        for i, page_candidate in enumerate(self.config.page_cache):
            if page_candidate == OPENAPI_SPEC_PLACEHOLDER:
                page_data = self.config["pages"][i]
                logger.debug("loading API spec: {pg}".format(pg=page_data))
            elif page_candidate == NOT_LOADED_PLACEHOLDER:
                page_data = self.config["pages"][i]
                # A not-loaded page is fine as long as this target doesn't
                # need it.
            else:
                page_data = page_candidate.data

            if not self.should_include(page_data):
                continue # Skip out-of-target pages;
            if page_candidate == NOT_LOADED_PLACEHOLDER:
                recoverable_error("Requires a page that failed to load: %s" %
                                  page_data, self.config.bypass_errors)
                continue # If we bypass errors, just omit the unloaded page

            # Expand OpenAPI Spec placeholders into full page lists
            if OPENAPI_SPEC_KEY in page_data.keys():
                try:
                    swagger_pages = self.expand_openapi_spec(page_data)
                    logger.debug("Adding generated OpenAPI reference pages: %s" %
                                    [p.data["name"] for p in swagger_pages])
                    pages += swagger_pages
                except Exception as e:
                    recoverable_error("Error when parsing OpenAPI definition %s: %s" %
                                      (page_data, e), self.config.bypass_errors)
                    # Omit the API def from the page list if an error occurred

            # Load cached page object; pass on target key-values,
            # then add it to the list
            else:
                merge_dicts(self.data, page_data, RESERVED_KEYS_TARGET)
                # Special case for filters; concatenate filter lists,
                # with target's filters first.
                if "filters" in self.data:
                    page_candidate.gain_filters(self.data["filters"])
                pages.append(page_candidate)

        # Check for pages that would overwrite each other
        html_outs = set()
        for p in pages:
            if "html" not in p.data.keys():
                logger.error("page has no html somehow? %s"%p.data)
            if p.data["html"] in html_outs:
                recoverable_error(("Repeated output filename '%s'. The earlier "+
                    "instances will be overwritten") % p.data["html"],
                    self.config.bypass_errors)
            html_outs.add(p.data["html"])

        self.pages = pages

        # Special case for ad-hoc targets with one page: rename to page name
        # if no title was provided.
        if len(self.pages) == 1 and self.name == UNTITLED_TARGET:
            self.name = self.pages[0].data["name"]
            self.data["display_name"] = self.name

        self.find_hierarchy()
        return pages

    def find_hierarchy(self):
        """
        Adds "children" arrays to pages to mirror "parent" links.
        """
        for p in self.pages:
            if "parent" in p.data.keys():
                try:
                    parent = next((pg for pg in self.pages if pg.data["html"] == p.data["parent"]))
                except StopIteration:
                    logger.warning("parent '%s' value not found in this target"%p.data["parent"])
                    continue

                if "children" in parent.data.keys():
                    if type(parent.data["children"]) != list:
                        logger.warning("hierarchy: page '%s' has explicit children field, not modifying."%parent.data["html"])
                        continue
                    else:
                        # Add this child to the parent's existing list if it's
                        # not already there.
                        if p.data not in parent.data["children"]:
                            parent.data["children"].append(p.data)
                else:
                    # Start a new child list at the parent
                    parent.data["children"] = [p.data]

            if "children" not in p.data.keys():
                # Start an empty list of children
                p.data["children"] = []

        for p in self.pages:
            # Separate loop so we don't miss it where the parent isn't in-target
            p.data["is_ancestor_of"] = self.make_ancestor_lookup(p)

    @staticmethod
    def make_ancestor_lookup(p):
        # logger.debug("defining is_ancestor_of for %s"%p)
        def is_ancestor_of(html):
            if "children" not in p.data.keys():
                return False
            if type(p.data["children"]) != list:
                return False
            for kid in p.data["children"]:
                if kid["html"] == html:
                    return True
                if kid["is_ancestor_of"](html):
                    return True
            return False
        return is_ancestor_of

    def categories(self):
        """Produce an ordered, de-duplicated list of categories from
           this target's page list"""
        categories = []
        for page in self.pages:
            if "category" in page.data and page.data["category"] not in categories:
                categories.append(page.data["category"])
        logger.debug("categories: %s" % categories)
        return categories
