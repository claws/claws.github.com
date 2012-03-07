---
layout: post
title: "Jekyll Post Excerpts Plugin And Also Without A Plugin For use On Github pages"
tags: 
- blog
meta-description: "Creating a post excerpt filter plugin for Jekyll and the same functionality for use on Github pages without a plugin"
---

_Disclaimer: I've only just started playing with Jekyll. This may be completely off track but it worked for me - until I find something better._

<!-- excerpt start -->
While setting up this blog I wanted to be able to display post excerpts on the main page. I found a few different methods but none really met my needs.

- I wanted to be able to use a small section of the post itself as the excerpt. 
- I didn't want to duplicate the post excerpt section. 
- I didn't want to push it through the Liquid strip_html filter because the output didn't look very nice. 
- I didn't want to arbitrarily truncate the text at a certain character limit either.
<!-- excerpt end -->

I found an example of a Jekyll/Liquid plugin and modified it to suit my needs. The result is a small Jekyll filter plugin that extracts text between two html comments that can be used to populate the post extract on the main page. This worked really well locally where I was testing the web site before uploading it to Github. 

I got everything working locally and was quite pleased. I then pushed the changes to github and FAIL. I got a notification stating <code>unable to run jekyll</code>. That is a cryptic error - completely useless for me to diagnose the cause of the problem. 

After searching around I think it was because Github do not allow plugins to run arbitrary functions on their servers - fair enough too actually. I must have missed the part where that was documented. That would perhaps explain why I didn't come arcoss anyone doing this before me. Still this might be useful to someone running the site on their own server.

<script src="https://gist.github.com/1964919.js"> </script>

<hr />

So I spent some time removing the references to the plugins so that they would not be run again. This didn't seem to be enough though. I found that I actually had to entirely remove the <code>_plugin</code> directory and it's contents for the uploaded content to be parsed and visible on my github pages site.

I needed to come up with another way of creating the excerpts. 

I investigated the Liquid filters further and worked out a way to use the strip function to the same effect as the plugin.

<script src="https://gist.github.com/1965992.js"> </script>

<hr />

Once again this worked fine locally so I pushed it to Github - only to find that the strip function does not appear to be working in the version of Liquid used at Github. This is detailed [here](https://github.com/mojombo/jekyll/issues/502) and [here](https://github.com/Shopify/liquid/issues/92).

So for the time being I have no excerpts.

