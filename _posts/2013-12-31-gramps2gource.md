---
layout: post
title: "Gramps2Gource"
tags:
 - Gramps
 - Python
 - Gource
meta-description:
# Don't change the disqus identifier even if the url changes. It uniquely
# associates comments with the post.
disqus-identifier: "gramps2gource"
summary: This post details the gramps2gource utility script that creates Gource custom log files from Gramps data.
---

## Gramps2Gource

[Gramps](http://gramps-project.org/) is a Genealogy program written in Python. [Gource](https://code.google.com/p/gource/) is a visualisation tool for showing software version control changes over time.

<!-- excerpt start -->
**Gramps2Gource** combines Gramps and Gource to help produce a novel family history visualisation. It parses exported `.gramps` files to produce a Gource custom log file that contains the pedigree of a specified person. This file is then passed to Gource for rendering.
<!-- excerpt end -->

Currently the script produces a pedigree for the specified people. It starts with the specified person and then walks backwards through the pedigree tree. See the example video below:

<center><iframe width="560" height="315" src="//www.youtube.com/embed/sPtTTv6d0s8" frameborder="0" allowfullscreen></iframe></center>

An obvious potential addition would be to specify a person and walk forwards in time to see all their offspring.

I initially started thinking about this concept while investigating ways to visualise the code base at work where we are using Clearcase. Gource does not support Clearcase by default, but there is a mechanism called custom log format whereby non-supported SCMs can be augmented to output a custom history log that allows Gource to display the results.

After working out how to generate the custom log format I realised that I might be able to use the same approach to create a novel visualisation for my family history database.

I had previously written a parser to walk over an exported `.gramps` file to produce lifeline paths showing an individuals movements around the Earth as KMZ files for viewing on Google Earth. The exported `.gramps` files were simpler for me to parse than to integrate my parser into the Gramps application to get access to the real database. So I started with this simple `.gramps` file parser.

The first step was to extract pedigree data for a specific person from my Gramps database and then to generate a custom format output file suitable for passing as input to the Gource visualisation tool.

The results really depend on your database content. If it is not well managed and consistent then I would not expect particularly impressive results. I'm pretty happy with the results from my database.

I may investigate integrating this into a Gramps plugin one day.
