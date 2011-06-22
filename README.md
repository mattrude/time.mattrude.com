# time.mattrude.com #

This is my timeservers web site's source repository.  This repository doesn't contain the code for NTP, but instead the code to run the actual website.

## About ##

This site uses rrdtools to build and display usage graphs.  rrdtools is required to be installed on the host server before the graphs may be created.

There is also a decent amount of back end setup that needs to happen before the graphs may be displayed, please see the README in the scripts directory for those instructions.

## Installing ##

The install proccess for this project at this time is a bit cumbersome.  Currently it assumes all files are stored in `/var/www/time.mattrude.com`.  This will change in the future, but for now, it will be just easiest to create that director on your system.

To install, first you need to add a cron entry for the RRD graphs.

    */5 * * * * /var/www/time.mattrude.com/scripts/do-xntp > /dev/null 2&>1

After adding the cron job, you may add your NTP Servers. To add your NTP servers, start by going into the scripts directory.  Once in the scripts directory, run the `do-newntpstat` followed by the name of the computer, similar to below.

    ./do-newntpstat time.example.com

### Rebuilding CSS ###
To Rebuild the css file, first download and install the [YUI Compressor](https://github.com/yui/yuicompressor), then run:

    java -jar yuicompressor.jar style.dev.css > style.css
