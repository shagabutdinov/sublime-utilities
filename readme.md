# Sublime Utilities plugin

Minor utilities for building snippets and plugins.


### Installation

This plugin is part of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
plugin set. You can install sublime-enhanced and this plugin will be installed
automatically.

If you would like to install this package separately check "Installing packages
separately" section of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
package.


### Features

  - "replace_region" - replace given region with given text; arguments: region
    ([start, end]) - region to replace, text (string) - string to put to region.

  - "replace_text_by_regexp" - replace text from start of line to begin of
    selection by given regexp; arguments: regexp (string) - expression to hit,
    replacement (string) - string to put instead of matched (backreferences \\1
    are supported); if no regexp matches no replacemenet will be made.

  - "insert_text" - insert text to given point; arguments: point (int), text
    (string)

  - "delete_selection" - delete selected region; arguments: none


### Usage

Run commands listed above from keyboard shortcut, macro-file, snippet or other
plugin.

Example keymap:

  ```
  {
    "keys": ["ctrl+f5"],
    "command": "insert_text",
    "args": {
      "point": 0,
      "text": "<?php"
    }
  }
  ```