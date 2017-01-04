#!/usr/bin/env python

import sh

"""
This command can show much better log, and try to write git commit as a story.
"""

print(sh.git.log("--format=oneline", "--abbrev-commit"))
