
from Expression import expression
import re

def find_this_arg(view, star = None):
  expr = 'func\s*\((.*?)\)'
  result = expression.find_match(view, view.sel()[0].a, expr,
    {'backward': True, 'scope': 'keyword.other.go'})
  result = result or expression.find_match(view, view.sel()[0].a, expr,
    {'backward': False, 'scope': 'keyword.other.go'})
  result = result or expression.find_match(view, 0, 'type (\w+)',
    {'backward': False, 'scope': 'keyword.other.go'})

  if result != None:
    result = result.group(1)
  else:
    result = ""

  if star == True:
    result = re.sub(r'(\s)(\w+)$', '\\1*\\2', result)
  elif star == False:
    result = re.sub(r'(\s)\*(\w+)$', '\\1\\2', result)

  return result

def find_this_type(view, star = None):
  expr = 'func\s*\(.*?\s(\w+)\)'
  result = expression.find_match(view, view.sel()[0].a, expr,
    {'backward': True, 'scope': 'keyword.other.go'})
  result = result or expression.find_match(view, view.sel()[0].a, expr,
    {'backward': False, 'scope': 'keyword.other.go'})
  result = result or expression.find_match(view, 0, 'type (\w+)',
    {'backward': False, 'scope': 'keyword.other.go'})

  if result != None:
    result = result.group(1)
  else:
    result = ""

  if star == True:
    result = re.sub(r'(\s)(\w+)$', '\\1*\\2', result)
  elif star == False:
    result = re.sub(r'(\s)\*(\w+)$', '\\1\\2', result)

  return result