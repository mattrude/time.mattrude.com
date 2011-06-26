# NTP Scripts #

I have written a set of scripts that use "ntpq -c rv" probes to gather statistics from the various servers. I'm using a list-of-systems mode with auto generation of the index.html file. The first script to run is do-newntpstat to create the database. Make sure the database that is created gets moved to the place where the next script can find it. Add your host name(s) to the list-of-systems and run do-mung-newhost to create the index.html file. The script takes template files 1. index-head, 2. template, 3. index-tail and churns out the updated web page. The cron job then runs do-xntp to update the png data images. A further script do-rrd-update probes the ntp-dev servers and extracts the reqired data it then uses to populate the rrd database.

http://www.wraith.sf.ca.us/ntp/index.html#monitoring

## Installing ##

The install proccess for this project at this time is a bit cumbersome.  Currently it assumes all files are stored in `/var/www/time.mattrude.com`.  This will change in the future, but for now, it will be just easiest to create that director on your system.

To install, first you need to add a cron entry for the RRD graphs.

    */5 * * * * <path-to-source>/scripts/do-xntp > /dev/null 2&>1

After adding the cron job, you may add your NTP Servers. To add your NTP servers, start by going into the **scripts/** directory.  Once in the scripts directory, run the `do-newntpstat` followed by the name of the computer, similar to below.

    ./do-newntpstat time.example.com

Lastly, if you wish to also count the current number of clients per server, run the below to lines.

    echo "/usr/bin/perl -w <path-to-source>/scripts/ntpclientsd -dump /var/log/ntpstats/ntp_stats.dump >> /var/log/ntpstats/ntp_stats.log 2>&1 &" >> /etc/rc.local
    /usr/bin/perl -w <path-to-source>/scripts/ntpclientsd -dump /var/log/ntpstats/ntp_stats.dump >> /var/log/ntpstats/ntp_stats.log 2>&1 &


## Adding a new server ##

To add a new server to the site, run `do-newntpstat <server_name>`
