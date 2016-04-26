import sublime
import sublime_plugin
import re

try:
  from Expression import expression
  from Context import context
except Exception:
  print("Some dependencies has not been imported for Utilities package; " +
    "some utilities functionality will not be availiable")

class ReplaceText(sublime_plugin.TextCommand):
  def run(self, edit, region, text):
    self.view.replace(edit, sublime.Region(*region), text)

class ReplaceTextByRegexp(sublime_plugin.TextCommand):
  def run(self, edit, regexp, replacement, key = 'preceding_begin'):
    for sel in reversed(self.view.sel()):

      if key == 'preceding_begin':
        region = sublime.Region(self.view.line(sel.begin()).a, sel.begin())
      elif key == 'following_end':
        region = sublime.Region(sel.end(), self.view.line(sel.end()).b)
      else:
        raise Exception('Unkonwn text type should be "' + key + '"')

      initial = self.view.substr(region)
      text = re.sub(regexp, replacement, initial)
      if text != initial:
        self.view.replace(edit, region, text)

class InsertText(sublime_plugin.TextCommand):
  def run(self, edit, text, point = None):
    if point == None:
      point = self.view.sel()[0].begin()

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

class RemoveNestingCloser(sublime_plugin.TextCommand):
  def run(self, edit):
    for sel in reversed(self.view.sel()):
      nesting = expression.get_nesting(self.view, sel.begin(), 2048)
      if nesting == None:
        continue

      self.view.erase(edit, sublime.Region(nesting[1], nesting[1] + 1))

class RunCommands(sublime_plugin.TextCommand):
  def run(self, edit, commands):
    for command in commands:
      ignored = (
        'context' in command and
        not context.check(self.view, command['context'])
      )

      if ignored:
        continue

      args = {}
      if 'args' in command:
        args = command['args']

      self.view.run_command(command['command'], args)

def ensure_line_before(view, edit, ignore):
  for sel in reversed(view.sel()):
    start = view.line(sel.begin()).a - 1
    previous_line = re.sub(r'\s', '', view.substr(view.line(start)))

    if previous_line == '':
      return

    for ignore_value in ignore:
      if previous_line.endswith(ignore_value):
        return

    view.insert(edit, start, "\n")

class EnsureLineBefore(sublime_plugin.TextCommand):
  def run(self, edit, ignore = ['{', '[', 'begin']):
    ensure_line_before(self.view, edit, ignore)

def ensure_line_after(view, edit, ignore):
  for sel in reversed(view.sel()):
    end = view.line(sel.begin()).b + 1
    next_line = re.sub(r'\s', '', view.substr(view.line(end)))

    if next_line == '':
      return

    for ignore_value in ignore:
      if next_line.startswith(ignore_value):
        return

    view.insert(edit, end, "\n")

class EnsureLineAfter(sublime_plugin.TextCommand):
  def run(self, edit, ignore = ['}', ']', 'end']):
    ensure_line_after(self.view, edit, ignore)

class EnsureLinesAround(sublime_plugin.TextCommand):
  def run(self, edit, ignore_after = ['}', ']', 'end'],
    ignore_before = ['{', '[', 'begin']):

    ensure_line_before(self.view, edit, ignore_before)
    ensure_line_after(self.view, edit, ignore_after)

class EnsureSpaceBefore(sublime_plugin.TextCommand):
  def run(self, edit, space_char = ' ', ignored = ['(', '{', '[']):
    for index, _ in enumerate(self.view.sel()):
      sel = self.view.sel()[index]

      begin = sel.begin()
      prefix = self.view.substr(sublime.Region(self.view.line(begin).a, begin))
      match = re.search(r'(\S?)(\s*)$', prefix)

      target = space_char
      if match.group(1) in ignored:
        target = ''

      ignore = (
        match.start() == 0 or
        match.group(2) == target
      )

      if ignore:
        continue

      if match.group(2) == '':
        self.view.insert(edit, begin, target)
      else:
        region = sublime.Region(begin - len(match.group(2)), begin)
        self.view.replace(edit, region, target)

class EnsureSpaceAfter(sublime_plugin.TextCommand):
  def run(self, edit, space_char = ' ', ignored = [')', '}', ']', ',', ':']):
    sels = []

    for index, _ in enumerate(self.view.sel()):
      sel = self.view.sel()[index]
      end = sel.end()
      prefix = self.view.substr(sublime.Region(end, self.view.line(end).b))

      match = re.search(r'^(\s*)(\S?)', prefix)

      target = space_char
      if match.group(2) in ignored:
        target = ''

      if match.group(1) != target:
        if match.group(1) == '':
          self.view.insert(edit, end, target)
        else:
          region = sublime.Region(end, end + len(match.group(1)))
          self.view.replace(edit, region, target)

      sels.append(sel)

    self.view.sel().clear()
    self.view.sel().add_all(sels)

class EnsureSpacesAround(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.run_command('ensure_space_before')
    self.view.run_command('ensure_space_after')