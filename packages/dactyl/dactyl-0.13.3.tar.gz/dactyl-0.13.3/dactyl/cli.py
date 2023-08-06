#!/usr/bin/env python3
from dactyl.common import *
import argparse

class DactylCLIParser:
    UTIL_BUILD = "Generate static site from markdown and templates."
    UTIL_LINKS = "Check files in this repository for broken links."
    UTIL_STYLE = "Check content files for style issues."

    def __init__(self, utility):
        """Specify commandline usage and parse arguments"""
        parser = argparse.ArgumentParser(description=utility)

        noisiness = parser.add_mutually_exclusive_group(required=False)
        noisiness.add_argument("--quiet", "-q", action="store_true",
                            help="Suppress status messages")
        noisiness.add_argument("--debug", action="store_true",
                            help="Print debug-level log messages")

        parser.add_argument("--config", "-c", type=str,
                            help="Specify path to an alternate config file.")
        parser.add_argument("--version", "-v", action="store_true",
                            help="Print version information and exit.")
        parser.add_argument("--bypass_errors", "-b", action="store_true",
                            help="Continue if recoverable errors occur")

        if utility in (self.UTIL_BUILD, self.UTIL_STYLE):
            parser.add_argument("--target", "-t", type=str,
                help="Use the specified target (from the config file).")

        if utility == self.UTIL_BUILD:
            build_mode = parser.add_mutually_exclusive_group(required=False)
            build_mode.add_argument("--pdf", nargs="?", type=str,
                                const=PDF_USE_DEFAULT, default=NO_PDF,
                                help="Output a PDF to this file. Requires Prince.")
            build_mode.add_argument("--md", action="store_true",
                                help="Output markdown only")
            build_mode.add_argument("--html", action="store_true", default=True,
                                help="Output HTML files (the default)")
            build_mode.add_argument("--es", action="store_true",
                                help="Output JSON for ElasticSearch upload")
            # HTML is the default mode

            static_files = parser.add_mutually_exclusive_group(required=False)
            static_files.add_argument("--copy_static", "-s", action="store_true",
                        help="Copy all static files to the out dir",
                        default=False)
            static_files.add_argument("--no_static", "-S", action="store_true",
                        help="Don't copy any static files to the out dir",
                        default=False)
            static_files.add_argument("--template_static", "-T", action="store_true",
                        help="Copy only templates' static files to the out dir",
                        default=False)
            static_files.add_argument("--content_static", "-C", action="store_true",
                        help="Copy only the content's static files to the out dir",
                        default=False)
            parser.add_argument("--es_upload", nargs="?", type=str,
                                const=ES_USE_DEFAULT, default=NO_ES_UP,
                                help="Upload documents to ElasticSearch cluster "+
                                "at this URL (http://localhost:9200 by default). "+
                                "Ignored when making PDFs.")
            parser.add_argument("--leave_temp_files", action="store_true",
                                help="Leave temp files in place (for debugging or "+
                                "manual PDF generation). Ignored when using --watch",
                                default=False)
            parser.add_argument("--list_targets_only", "-l", action="store_true",
                                help="Don't build anything, just display list of "+
                                "known targets from the config file.")
            parser.add_argument("--only", type=str, help=".md or .html filename of a "+
                                "single page in the config to build alone.")
            parser.add_argument("--out_dir", "-o", type=str,
                            help="Output to this folder (overrides config file)")
            parser.add_argument("--pages", type=str, help="Markdown file(s) to build "+\
                                "that aren't described in the config.", nargs="+")
            parser.add_argument("--openapi", type=str, help="OpenAPI spec file "+
                                "to generate docs from.")
            parser.add_argument("--no_cover", "-n", action="store_true",
                                help="Don't automatically add a cover / index file.")
            parser.add_argument("--skip_preprocessor", action="store_true", default=False,
                                help="Don't pre-process Jinja syntax in markdown files")
            parser.add_argument("--template_strict_undefined", action="store_true",
                                help="Raise an error on undefined variables in "+
                                "template syntax.")
            parser.add_argument("--pp_strict_undefined", action="store_true",
                                help="Raise an error on undefined variables in "+
                                "preprocessor syntax.")
            parser.add_argument("--title", type=str, help="Override target display "+\
                                "name. Useful when passing multiple args to --pages.")
            parser.add_argument("--vars", type=str, help="A YAML or JSON file with vars "+
                                "to add to the target so the preprocessor and "+
                                "templates can reference them.")
            parser.add_argument("--watch", "-w", action="store_true", default=False,
                                help="Watch for changes and re-generate output. "+\
                                "This runs until force-quit.")
            parser.add_argument("--http_port", type=int, default=DEFAULT_SERVER_PORT,
                                help="Use this port for HTTP server (when "+\
                                "building PDFs.) Use '0' for no server (may not "+\
                                "work well with PDFs containing absolute links)")
            parser.add_argument("--legacy_prince", action="store_true",
                                help="When building PDFs, disable options that aren't"+\
                                "supported by older versions of Prince.",
                                default=False)

        elif utility == self.UTIL_LINKS:
            parser.add_argument("-o", "--offline", action="store_true",
                help="Check local anchors only")
            parser.add_argument("-d", "--dir", type=str, default=None,
                help="Check the specified dir (otherwise use configured out_dir)")
            parser.add_argument("-s", "--strict", action="store_true",
                help="Exit with error even on known problems")
            parser.add_argument("-n", "--no_final_retry", action="store_true",
                help="Don't wait and retry failed remote links at the end.")
            prefixes = parser.add_mutually_exclusive_group(required=False)
            prefixes.add_argument("-p", "--prefix", type=str, default="/",
                help="Assume site starts at this path. Must start with '/'")
            prefixes.add_argument("--no_prefix", action="store_true", default=False,
                help="Don't check absolute links")

        if utility == self.UTIL_STYLE:
            parser.add_argument("--only", type=str, help=".html filename of a "+
                                "single page in the config to check alone.")


        self.cli_args = parser.parse_args()
