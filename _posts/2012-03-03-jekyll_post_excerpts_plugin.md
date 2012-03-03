---
layout: post
title: "Jekyll Post Excerpts Plugin"
tags: 
- blog
meta-description: "Creating a post excerpt filter plugin for Jekyll"
---

_Disclaimer: I've only just started playing with Jekyll. This may be completely of track but it worked for me - until I find something better._

<!-- excerpt start -->
While setting up this blog I wanted to be able to display post excerpts on the main page. I found a few different methods but none really met my needs.

I wanted to be able to use a small section of the post itself as the excerpt. I didn't want to duplicate the post excerpt section. I didn't really want to push it through the strip_html filter because the output didn't look very nice. I didn't want to arbitrarily truncate the text at a certain character limit either.

I found an example of creating a Jekyll/Liquid plugin and modified it to suit my needs. The result is a small Jekyll plugin that extracts text between two html comments that can be used to populate the post extract object on the main page. 

You can find it in this [gist](https://gist.github.com/1964919).
<!-- excerpt end -->

<hr />
The example below shows the contents of the plugin which should be added to your <code>_plugins</code> directory:
{% gistnocache 1964919 excerpt.rb %}

<hr />
The example below how to use the excerpt delimiters within a post:

{% gistnocache 1964919 2012-03-03-demo.md %}

<hr /> 
The example below shows how to use the excerpt filter to extract the excerpt from the post and display it amongst a listing of posts:

{% gistnocache 1964919 index.html %}


