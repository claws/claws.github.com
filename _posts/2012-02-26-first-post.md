---
layout: post
title: "Test Post"
meta-description: "A simple test post"
disqus-identifier: "test_post"
tags: 
- python
summary: Just testing
---

<!-- excerpt start -->
This is an excerpt from the test post.
<!-- excerpt end -->

Testing code section and highlighting:

    {% highlight python %}

    import this
    
    class Test(object):
        """
        Test docstring
        """
        def __init__(self, name):
            self._name = name
    
        @property
        def name(self):
            return "The test name: %s" % self._name
    
    {% endhighlight %}

Test embedding Youtube video...

<iframe width="640" height="360" src="http://www.youtube.com/embed/FJ7QsEytQq4?rel=0" frameborder="0" allowfullscreen></iframe>

