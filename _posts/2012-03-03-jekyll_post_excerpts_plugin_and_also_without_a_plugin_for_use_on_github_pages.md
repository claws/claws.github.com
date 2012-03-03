---
layout: post
title: "Jekyll Post Excerpts Plugin And Also Without A Plugin For use On Github pages"
tags: 
- blog
meta-description: "Creating a post excerpt filter plugin for Jekyll and the same functionality for use on Github pages without a plugin"
---

_Disclaimer: I've only just started playing with Jekyll. This may be completely of track but it worked for me - until I find something better._

<!-- excerpt start -->
While setting up this blog I wanted to be able to display post excerpts on the main page. I found a few different methods but none really met my needs.

I wanted to be able to use a small section of the post itself as the excerpt. I didn't want to duplicate the post excerpt section. I didn't really want to push it through the strip_html filter because the output didn't look very nice. I didn't want to arbitrarily truncate the text at a certain character limit either.

I found an example of creating a Jekyll/Liquid plugin and modified it to suit my needs. The result is a small Jekyll plugin that extracts text between two html comments that can be used to populate the post extract object on the main page. 

You can find it in this [gist](https://gist.github.com/1964919).
<!-- excerpt end -->

<hr />


_Update: So yeah, I was off track. I got everything working locally, sweet. Pushed to github and FAIL. No plugins allowed - fair enough too actually. That would perhaps explain why I didn't come arcoss anyone doing this before me. Still this might be useful to someone running the site on their own server._

<script src="https://gist.github.com/1964919.js"> </script>


<hr />

To get this working on Github pages without a plugin I applied the same functionality to a line in the <code>index.html</code> page. It can be found in this [gist](https://gist.github.com/1965992).

<script src="https://gist.github.com/1965992.js"> </script>

After making the first round of changes which were based on plugins I kept getting <code>unable to run jekyll</code> errors whenever I tried to push. I managed to resolve this by removing the _plugins directory and its content. Correlation/causation? I think these were causing the problems but I guess I'll never know.

