Changelog
=========

1.1.15
------
    - Remove pinned version of pathlib.

1.1.14
------
    - Dependencies pinned so that Docker file now builds again (#107).

1.1.13
------
    - Sigh. Python package dependencies are really something (#107).

1.1.12
------
    - Add pathlib to dependencies (#107).

1.1.11
------
    - Another attempt to fix a syntax error in setuptools.

1.1.10
------
    - Pinned setuptools==40.8.0 because of syntax error in newer version (#107).

1.1.9
-----
    - Implemented #100 - date format in field 588.
    - Fixed deprecated whois lookup call (#101).

1.1.8
-----
    - Fixed #95 - bug in UDP logger / DNS name resolution.
    - Logger (#87) rewritten to better architecture.

1.1.7
-----
    - Implemented HTML lang and xml:lang parameters parsing (#88).

1.1.6
-----
    - Added support for Sentry (#92).

1.1.5
-----
    - URL added to logging.
    - build_keyword_index.py script fixed to replace HTML entities.
    - Downloaded additional 40 thousand records from aleph. Keywords regenerated.
    - HTML escaping disabled in the MRC template.

1.1.4
-----
    - Fixed IP address for the structured logger.

1.1.3
-----
    - Fixed metadata for the package.

1.1.2
-----
    - Improved logger capability with structured logs.
    - Creation date detector updated (#89) to reflect newest changes in 3rd party API.
    - Added server for structured logger.

1.1.1
-----
    - Fixed `download_as_file()` decorator to not to try to return result as JSON.

1.1.0
-----
    - Attempt to remove ZODB/ZEO, because it is horribly broken.

1.0.0 - 1.0.6
-------------
    - Connected with Seeder. First officaly working, production ready version.
    - Added better connection to Seeder.
    - #85: Fixed bug in the whois parsing.
    - #85: Updated API link for the memento web.
    - Dockerfile migrated to ubuntu 16.04.
    - Removed duplicate line from MANIFEST.in.
    - Fixed bug in error log path.
    - #86: Added custom error log path / option to switch to stderr.
    - Last attempt to pin requirements to older version.

0.4.1 - 0.4.5
-------------
    - Added missing MANIFEST.in.
    - Added `settings.ZEO_SERVER_PATH`.
    - ``conf/`` directory moved to ``templates/``.
    - Template updated accordingly to #78.
    - #80: Language in 008 is now parsed from user input.

0.4.0
-----
    - Beta version, almost ready for production use.
    - #26: Added more of the admin documentation.
    - #26: Added a lot of informations about administration of the project.
    - Setup / bin scripts updated.
    - Added argparse interface to the wa_kat_server.py.
    - Removed no longer needed file.
    - #26: Admin docs moved to admin_manual.rst.
    - #26: Added description of Hidden log. Admin doc moved to own file.
    - #26: Added description of the buttons.
    - #26: Added description of Periodicit, Frequency and Rules.
    - #26: Added description of Lanuage and Annotation.
    - #26: Added Konspekt / Subkonspekt description.
    - #26: Added keyword widget description.
    - #26: Added Place info.
    - Fixed bug in keywords.
    - #26: Fixed small bugs in dynamic help subsystem.
    - #26: Small fixes in manual.
    - #26: Added HelpOverlay, so user may now show quick help.
    - #26: Added Author picker documentation.
    - Added progressbar to Author picker.
    - #26: Added Publisher documentation.
    - #26: Added documentation for Subtitle and Creation date.
    - #26: Added description of Title.
    - #26: Added more documentation of progressbar.
    - url_progress_bar.png -> url_progressbar.png.
    - Added progressbar to ISSN request.
    - Fixed .reset() call on validation highlights.
    - #25: Added ISSN documentation. Added more documentation to URL.
    - #26: Added documentation for the URL field.
    - #26: Added wa_kat.png with screenshot of the app.
    - #26: Manual included to the index. Added basic description.
    - Added docstrings to overlay_controller.py. Fixed #25.
    - #25: Added docstrings to placeholder_handler.py.
    - #25: Added docstrings to progressbar.py.
    - #25: Added docstrings to shared.py.
    - #25: Added docstrings for output_picker.py.
    - #25: Added docstrings for log_view2.py.
    - #25: Added docstrings for input_controllericker.py.
    - #25: Added docstrings to conspect_handler.py.
    - #25: Added docstrings for dropdown handler.
    - #25: Added docstrings for errorbox.py.
    - #25: Added docstrings for author_picker.py.
    - #25: Added docstrings to author_picker.py.
    - AlephReaderAdapter refactored to AlephISSNReaderAdapter.
    - #25: Added docstrings for the wa_kat_main.py.
    - #25: Updated docstrings for rules_view.py.
    - #25: Added docstrings for view.py.
    - #25: Added docstrings for descritors.py.
    - #25: Fixed docstring for data_model.py.
    - #25: Fixed documentation.
    - bottle_index.py moved to rest_api/.
    - #25: Added docstrings of data_model.py.
    - #25: Added docstrings to settings.py.
    - Fixed bug in cleanup button.
    - #25: Removed no longer used file conspect_database.py.
    - #25: Fixed docstrings for worker.py.
    - Fixed height of the black overlay.
    - #25: Added docstrings to rest_api/__init__.py.
    - #25: Added docstrings to analyzers_api.py.
    - rest_api/__init__.py split to the rst_api/analyzers_api.py.
    - #25: Added docstrings to to_output.py.
    - #25: Added docstrings to aleph_api.py.
    - shared.RESPONSE_TYPE renamed to JSON_MIME.
    - #25: Added docstrings to shared.py.
    - Fixed HTML entity bug &apos; -> '.
    - #25: Undocumented some global variables, because extenzive spamming in HTML
    - #25: Added docstrings to keywords.py.
    - #25: Added docstrings for virtual_fs.py.
    - #26: Added links to the user manual.
    - #26: Added more placeholders to the manual.rst.
    - #33: Added question marks, which will open help (#26).
    - Fixed #73.
    - #25: Updated docstring for the convertors.rst.
    - #25: Added docstrings for mrc.py.
    - #25: Added docstrings for to_dc.py.
    - #25: Fixed invalid paths in .rst files for convertors.
    - #25: Added docstrings to iso_codes.py.
    - #25: Updated.
    - #25: Updated Author's docstring.
    - #25: Updated aleph connector docstring.
    - #25: Updated docstrings for connectors/.
    - #25: Added docstrings for init.
    - #25: Added docstrings to annotation_detector.py.
    - #25: Added docstrings to author_detector.py.
    - #25: Added docstrings to keyword_detector.py.
    - #26: Manual updated.
    - #25: Added docstrings to language_detector.py.
    - #25: Added docstrings to place_detector.py.
    - #25: Added docstrings to source_string.py.
    - #25: Added docstrings to title_detector.py.
    - #25: Added docstrings to creation_date_detector.py.
    - Added new requirement for `textblob` to implrove keyword matching.
    - #4: Improved creation date parsing. Removed duplicates.
    - #2: Slightly improved keyword parsing. Added docstrings (#25).
    - #26: Added first parts of the documentation.
    - Fixed bug in language detector. Languages should now occur only once.
    - Performance of keyword maching improved slightly. Fixed #2.
    - #2: Added _extract_keywords_from_text().
    - #2: Added better unicode decoder for analyzers.
    - #2: Added better utf / unicode handling to SourceString constructor.
    - #2: Added new precomputed dataset: KEYWORDS_LOWER.
    - #2: Added requirement for newer version of dhtmlparser.
    - Added red underline for all required elements.
    - Implemented get_creation_date_tags(). Closed #4.
    - #4: Implemented _get_whois_tags().
    - #4: Added new requirement for `pythonwhois`.
    - #4: settings.py: Added new variable WHOIS_URL.
    - Added transport of the 18'th char from 008 field. Closing #66.
    - #4: Implemented parsing of resources from the MementoWeb.org.
    - Fixed #72 - problem with redirects to pages with broken SSL.
    - #72: Added better logging of error messages.
    - #25: Added Sphinx documentation files for Dublin core convertor (#13).
    - Dublin core convertor integrated into the application. Closed #13.
    - #13: Added tests (#22).
    - #13: Reformatted. Added docstrings (#25).
    - #22: Added sketch of the DC tests (#13).
    - #13: Added parsing of the author.
    - #13: Added periodicity and place parsing.
    - #13: Imported in the convertors. Added docstring.
    - #13: Added processing of the keywords. Added url.
    - #13: Added dcterms:alternative, dcterms:created and DDC.
    - #13: Added parsing of title, publisher, description, language, issn & MDT.
    - #13: Added first sketch of to_dc().
    - #13: Added requirements to xmltodict and odictliteral.
    - Fixed bug in additional info getter. Closed #70, #71.
    - #70: Fixed bug in urlbar.
    - #66: Additional info is now transported to the output.
    - #66: Added new function - item_to_mrc().
    - #66: Added parsing of end_date to the aleph connector.
    - #66: Added better parsing of creation date.
    - #22, #66: Added tests of mrc convertor.
    - #66: Added val_to_mrc().
    - Added requirement for new version of marcxml-parser.
    - Fixed bug in setup.py.
    - #22: Fixed bugs in tests.
    - #25, #26: Documentation files updated.
    - #66: mrc_to_marc.py renamed to mrc.py, because new functions were added.
    - #66: Added dict_to_mrc().
    - #66: Added processing of the additional info in the frontend.
    - #66: Added reading of additional info from Aleph.

0.3.0
-----
    - Added Author picker and connection to Aleph.
    - Fixed lot of bugs, most of the components are now working.
    - setup.py: Added definition of scripts.
    - Added wa_kat prefix to all scripts in /bin.
    - Added timeout for seeder and some error handling. Closed #16.
    - Added docstrings (#25).
    - #16: Added settings.SEEDER_TIMEOUT.
    - #16: Added handling of Seeder's avaliability (#51).
    - Fixed bugs in .reset(). Closed #69.
    - #69: Added cabability of basic .reset().
    - #25: Added docstring.
    - #51: Added adapters for reading data from Seeder. Basic dataset now works.
    - #51: Added transport of Seeder's data to the frontend.
    - #51: Fixed bugs in Seeder connector code.
    - #25: Added docstrings and other comments.
    - Added support for subtitle. Closed #64.
    - Added updated dataset. Fixed #68.
    - #68: Added skipping of deprecated records.
    - #68: Fixed logic od the building of keyword cache.
    - #68: Implemented better parser of keywords.
    - Naming convention changed.
    - build_keyword_index.py renamed to wa-kat_build_keyword_index.py.
    - #51: Added parts of the connector to the Seeder.
    - Removed unused space.
    - #68: Fixed case, when the english equivalent is not available.
    - #51: issn added to the data model.
    - Removed no longer required file.
    - #51: Seeder code moved to connectors/seeder.py.
    - #32: Virtual fs / conspectus code optimized for performance. Fixed #67.
    - Added custom headers for requests (#24) and Authentication headers (#51).
    - Custom headers are now used for analysis. Fixed #24.
    - #32: Added more frontend logging.
    - #32: Rewritten to load API_PATH from settings.py / virtual fs.
    - #32: Periodes are now transported to frontend using virtual fs.
    - #32: Added new virtual fs / periodes.py.
    - #59: Fixed output template to include data from new conspect dict.
    - #59: Removed unused files and code replaced by new version.
    - #32, #59: Completely rewritten conspect handler code.
    - #32, #59: searchable_conspect class renamed to whole_conspect_subconspect.
    - #32: Added conspect code (#59). Virtual filesystem is now implemented.
    - #32: Implemented virtual fs / conspectus.py
    - #32: Optimized.
    - #32: GUI_TO_REST_PERIODE is now read from virtual fs / settings.py.
    - #32: settings.py are now available in virtual fs.
    - #32: Added first part of the virtual filesystem for brython configuration.
    - #51: Rules data added to output dataset.
    - #32: Author errors are now logged by LogView component.
    - Added special requested default value to creation_date. Fixed #65.
    - #59: Added processed JSON data. This will require rewrite of the web gui.
    - #59: Added script, which processes the dataset from Dan Kindl to JSON.
    - Removed unused file.
    - #59: Added dataset from Dan Kindl.
    - #32: Added loading gear animation.
    - #32: Progress bar rewritten to use as instance instead of static class.
    - Fixed minor bugs.
    - #32: Fixed problems with scrolling on elements shadowed by overlay.
    - Removed unused file.
    - Output template fixed to not require Author field. Closed #62.
    - #62: Restructured. Removed `required` flag from the Author picker.
    - #62: publisher_switcher.py renamed to author_switcher.py.
    - #62: Rewritten to make Publisher always visible and Author optional.
    - #24: Added settings.ANALYZER_USER_AGENT.
    - Adde new settings: NTK_ALEPH_URL. Fixed #61.
    - Random comment updated.
    - #51: REMOTE_INFO_URL renamed to SEEDER_TOKEN. Removed MOCK API.
    - #61: ISSN requests redirected to NTK's Aleph.
    - Changed python interpreter version description comment.
    - #58: Added support of authors into the output.
    - #58: Fixed bug in author picker.
    - #58: Removed debug prints and GUI elements.
    - #58: Fixed code for reading the author from aleph
    - Added alternative author descriptions to main page.
    - #58: Added nicer input text at the main page.
    - #58: Added corporation/person indicator to the output.
    - #58: Added better detection of persons/corporations.
    - Full Author record is now transported to the frontend.
    - Added another example with ISSN and author record.
    - Added more examples of authority records.
    - #58: Publisher is now put into the 264b.
    - #58: Author analysis are now put into the publisher field.
    - #58: Added descriptor protocol to AuthorPicker. Included to form data.
    - Added better handling of event propagation.
    - #58: Added rest of the logic for picking elements.
    - #58: Disabled autocomplete on author's search input.
    - Changelog updated.
    - #58: Added working connection to Aleph REST API (AuthorPickerAdapter).
    - #58: make_request() and func_on_enter() moved to components/shared.py.
    - #58: Added `Vybrat` button to Author input.
    - #58: Added sketch of the author picker.
    - #58: Added better style definition for author picker.
    - #58: Added GUI element for picking the authors.

0.2.0
-----
    - Amost working.
    - Fixed bug in validator of Publisher.

0.1.0
-----
    - Project created.
