#!/usr/bin/env python
#
# Inspired by https://gist.github.com/100171
#
# This script creates a new post in the ../_posts directory
# with default template content ready for user content to
# be added.
# 


import datetime
import os
import sys

post_template = """---
layout: post
title: \"%(title)s\"
tags: []
meta-description: 
---

<!-- except start -->

<!-- except end -->

"""


if __name__ == "__main__":

    script_filepath = os.path.abspath(os.path.expanduser(sys.argv[0]))
    scriptname = os.path.basename(script_filepath)
    repo_root = os.path.dirname(os.path.dirname(script_filepath))

    if len(sys.argv) == 1:
        print "Usage: %s \"New Post Title\"" % scriptname
        sys.exit(1)

    date_string = datetime.datetime.now().strftime("%Y-%m-%d")
    title = sys.argv[1]
    post_filename = os.path.join(repo_root, "_posts", "%s-%s.md" % (date_string, title.lower().replace(" ", "_")))

    if os.path.exists(post_filename):
        # very unlikely
        print "Duplicate post detected, change post title"
        sys.exit(1)

    fd = open(post_filename, 'w')
    fd.write(post_template % {'title':title})
    fd.close()

    print "Created new post file: %s" % post_filename

