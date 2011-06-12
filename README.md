# time.mattrude.com #

This is my timeservers web site's source repository.  This repository doesn't contain the code for NTP, but instead the code to run the actual website.

This site uses rrdtools to build and display usage graphs.  rrdtools is required to be installed on the host server before the graphs may be created.

There is also a decent amount of back end setup that needs to happen before the graphs may be displayed, please see the README in the scripts directory for those instructions.

## Installing ##

### Rebuilding CSS ###
To Rebuild the css file, first download and install the [YUI Compressor](https://github.com/yui/yuicompressor), then run:

    java -jar yuicompressor.jar style.dev.css > style.css
