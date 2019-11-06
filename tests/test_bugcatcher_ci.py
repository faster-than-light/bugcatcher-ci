import os
bugcatcher_ci = __import__('bugcatcher-ci')
ftl_sid = os.environ.get('FTL_SID') # Keep it secure!
ftl_project = os.environ.get('FTL_PROJECT') or 'BUGCATCHER CI'
# ftl = bugcatcher_ci.CI(ftl_sid, ftl_project)


def test_bad_params():
  ftl_sid = ""
  ftl_project = ""

  test_ftl = bugcatcher_ci.CI(ftl_sid, ftl_project)
  assert test_ftl

  sid = test_ftl.get_sid()
  assert not sid

  print("\nTesting codebase with BugCatcher API...")
  uploaded = test_ftl.push(ftl_project, ".")
  assert not uploaded

  tested = test_ftl.test(ftl_project, 'medium')
  assert not tested


def test_good_params():
  test_ftl = bugcatcher_ci.CI(ftl_sid, ftl_project)
  assert test_ftl

  sid = test_ftl.get_sid()
  assert sid

  print("\nTesting codebase with BugCatcher API...")
  uploaded = test_ftl.push(ftl_project, ".")
  assert uploaded

  tested = test_ftl.test(ftl_project, 'medium')
  assert tested


