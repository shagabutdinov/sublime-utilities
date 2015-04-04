import sublime
import sublime_plugin
import re

class ReplaceText(sublime_plugin.TextCommand):
  def run(self, edit, region, text):
    self.view.replace(edit, sublime.Region(*region), text)

class ReplaceTextByRegexp(sublime_plugin.TextCommand):
  def run(self, edit, regexp, replacement, text_type = 'preceding_begin'):
    for sel in reversed(self.view.sel()):

      if text_type == 'preceding_begin':
        region = sublime.Region(self.view.line(sel.begin()).a, sel.begin())
      elif text_type == 'following_end':
        region = sublime.Region(sel.end(), self.view.line(sel.end()).b)
      else:
        raise Exception('Unkonwn text type should be "' + text_type + '"')

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

class DeleteNextLine(sublime_plugin.TextCommand):
  def run(self, edit):
    for sel in reversed(self.view.sel()):
      line = self.view.line(sel)
      next_line = self.view.line(line.b + 1)
      self.view.erase(edit, sublime.Region(next_line.a - 1, next_line.b))

class PrintCurrentLine(sublime_plugin.TextCommand):
  def run(self, edit):
    for sel in reversed(self.view.sel()):
      line = self.view.line(sel)
      print(self.view.substr(line))