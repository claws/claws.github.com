---
layout: post
title: Test Post
tags: [python]
---

This is a test post.

Testing code section and highlighting:

<figure class='code'><figcaption><span>test.py</span></figcaption>
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
</figure>

