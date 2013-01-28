# Speech Analysis

A collection of scripts for generic speech (written speech) processing. 

## State of the Union

A script for processing all the United States State of the Union speeches from 1790 (Washington) to 2012 (Obama), using TF-IDF. This is based on work for an assignment at the JMSC (at the University of Hong Kong) [here](http://jmsc.hku.hk/courses/jmsc6041spring2013/2013/01/18/assignment-1-tf-idf/)

There are a few different ways you can use this script:

* Output the top terms for a specific year: `python <script name> -y 2000`
* Output the top terms grouped by decade beginning with a specific year: `python <script name> -d 1900`

Additionally, you can specify the number of terms to return, defaulting to 20: `python <script name> -d 1900 -t 5`
