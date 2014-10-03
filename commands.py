import sublime
import sublime_plugin
import re

class ReplaceText(sublime_plugin.TextCommand):
  def run(self, edit, region, text):
    self.view.replace(edit, sublime.Region(*region), text)

class ReplaceTextByRegexp(sublime_plugin.TextCommand):
  def run(self, edit, regexp, replacement, text_type = 'preceding_begin'):
    for sel in reversed(self.view.sel()):
      if text_type != 'preceding_begin':
        raise Exception('Text type should be "preceding_begin"; other types ' +
          'not supported yet; you can add support for other types at ' +
          'Utilities/commands.py')

      region = sublime.Region(self.view.line(sel.begin()).a, sel.begin())
      initial = self.view.substr(region)
      text = re.sub(regexp, replacement, initial)
      if text != initial:
        self.view.replace(edit, region, text)

class InsertText(sublime_plugin.TextCommand):
  def run(self, edit, point, text):
    self.view.insert(edit, point, text)

class DeleteSelection(sublime_plugin.TextCommand):
  def run(self, edit):
    for sel in reversed(self.view.sel()):
      self.view.erase(edit, sel)