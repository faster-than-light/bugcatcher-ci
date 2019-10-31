# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import subprocess
import bugcatcher as ftl
import json
import os

ftl_cmd = [
  "ftl",
  "--sid",
  os.environ['FTL_SID'],
  "--project",
  "CI Pipleline"
]
minimum_severity_to_fail = 'medium'

def test_with_bugcatcher():
  print("\nUploading updated code to BugCatcher...")
  push = subprocess.check_output([
    *ftl_cmd,
    "push",
    "."
  ])
  assert push
  print_bytes(push)

  print("\nRunning tests using BugCatcher...")
  test = subprocess.check_output([
    *ftl_cmd,
    "--json",
    "test"
  ])
  assert test
  print("\nBugCatcher results:\n")

  hits = json.loads( test.decode("utf8") )

  failed = False
  for hit in hits:
    start_line = hit['start_line']
    end_line = hit['end_line']
    test_suite_test = hit['test_suite_test']
    ftl_severity = test_suite_test['ftl_severity']
    ftl_short_description = test_suite_test['ftl_short_description']
    ftl_long_description = test_suite_test['ftl_long_description']
    code_name = hit['code']['name']
    print("\nSeverity: %s ===> %s (lines %s-%s)\n\t%s - %s" % (
      ftl_severity,
      code_name,
      start_line,
      end_line,
      ftl_short_description,
      ftl_long_description
    ))
    if not passes_severity(ftl_severity):
      failed = True
  
  assert not failed
  print("\nPASSING: All results are less than \"%s\" level severity." % minimum_severity_to_fail)
  

def passes_severity(severity):
  levels = [ 'low', 'medium', 'high' ]
  if severity not in levels:
    return True
  severity = levels.index(severity)
  min_severity = levels.index(minimum_severity_to_fail)
  return min_severity > severity


def print_bytes(b):
  p = b.decode("utf-8")
  assert p

  for row in p.split('\n'):
    print(row)

def test_success():
    assert True
    
