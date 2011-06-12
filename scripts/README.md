# NTP Scripts #

I have written a set of scripts that use "ntpq -c rv" probes to gather statistics from the various servers. I'm using a list-of-systems mode with auto generation of the index.html file. The first script to run is do-newntpstat to create the database. Make sure the database that is created gets moved to the place where the next script can find it. Add your host name(s) to the list-of-systems and run do-mung-newhost to create the index.html file. The script takes template files 1. index-head, 2. template, 3. index-tail and churns out the updated web page. The cron job then runs do-xntp to update the png data images. A further script do-ntp-rrdstats probes the ntp-dev servers and extracts the reqired data it then uses to populate the rrd database.

http://www.wraith.sf.ca.us/ntp/index.html#monitoring

## Installing ##

This site uses cron scripts to gather statistics from the diffrent servers and to build the graphs.   Add the following to your crontab:

    */5 * * * * <path_to_source>/scripts/do-xntp > /dev/null 2&>1

## Adding a new server ##

To add a new server to the site, run `do-newntpstat <server_name>`
