This is my timeservers web site's source repository.  This repository doesn't contain the code for NTP, but instead the code to run my actual time server website.

## About ##

This site uses rrdtools to build and display usage graphs.  rrdtools is required to be installed on the host server before the graphs may be created.

The below informaion is tailored for [Fedora](http://fedoraproject.org/) servers, but should be generic enough for most unix/linux systems.

The source for this project may always be found on my github repository: [https://github.com/mattrude/time.mattrude.com](https://github.com/mattrude/time.mattrude.com)

## Downloading ##

You may download this project directly from [github](https://github.com/mattrude/time.mattrude.com) the current truck may be downloaded as a [tar.gz](https://github.com/mattrude/time.mattrude.com/tarball/master) file, or a [zip](https://github.com/mattrude/time.mattrude.com/zipball/master) file.

* Version 1.0 [tar.gz](https://github.com/mattrude/time.mattrude.com/tarball/1.0) - [zip](https://github.com/mattrude/time.mattrude.com/zipball/1.0)

or you can always just download the full [git](http://git-scm.com) repository:

    git clone git://github.com/mattrude/time.mattrude.com.git

## Prerequisites ##
The requirements for running this project on your own site are pretty simple.

* [Apache](http://www.apache.org/) 2.2+
* [RRDtools](http://oss.oetiker.ch/rrdtool/doc/index.en.html) 1.4.4+
* [Markdown](http://daringfireball.net/projects/markdown/) 2.0+

So on a Fedora system, you may run:

    yum -y install rrdtools python-markdown

## Installing ##

The install proccess for this project at this time is a bit cumbersome.  Currently it assumes all files are stored in `/var/www/time.mattrude.com`.  This will change in the future, but for now, it will be just easiest to create that director on your system.

To install, first you need to add a cron entry for the RRD graphs.

    */5 * * * * <path-to-source>/scripts/do-xntp > /dev/null 2&>1

After adding the cron job, you may add your NTP Servers. To add your NTP servers, start by going into the **scripts/** directory.  Once in the scripts directory, run the `do-newntpstat` followed by the name of the computer, similar to below.

    ./do-newntpstat time.example.com

Lastly, if you wish to also count the current number of clients per server, run the below to lines.

    echo "/usr/bin/perl -w <path-to-source>/scripts/ntpclientsd \
      -dump /var/log/ntpstats/ntp_stats.dump >> /var/log/ntpstats/ntp_stats.log 2>&1 &" >> /etc/rc.local
    /usr/bin/perl -w <path-to-source>/scripts/ntpclientsd \
      -dump /var/log/ntpstats/ntp_stats.dump >> /var/log/ntpstats/ntp_stats.log 2>&1 &

### Apache Config ###

    yum -y install httpd perl-CGI

The Apache configuration for virtual hosts is pretty simple. The only trick is setting the cgi directory.

    <VirtualHost *:80>
        ServerName time.example.com
        DocumentRoot /var/www/time.example.com
        CustomLog logs/time.example.com.access_log combined
        ErrorLog logs/time.example.com.error_log
        <Location /bin>
          Options Indexes FollowSymLinks
          Options +ExecCGI
          Order allow,deny
          Allow from all
          AddHandler cgi-script .cgi
        </Location>
    </VirtualHost>

### Lighttpd Config ###

Installing [Lighttpd](http://www.lighttpd.net/) on a Fedora system is pretty simple.

    yum -y install lighttpd lighttpd-fastcgi

After Lighttpd is installed, you need to configure it.

    server.document-root = "/var/www/time.example.com/" 
    server.port = 80
    
    server.username = "www" 
    server.groupname = "www" 
    
    mimetype.assign = (
      ".html" => "text/html", 
      ".txt" => "text/plain",
      ".jpg" => "image/jpeg",
      ".png" => "image/png" 
    )
    
    static-file.exclude-extensions = ( ".fcgi", ".php", ".rb", "~", ".inc" )
    index-file.names = ( "index.html" )


### Rebuilding CSS ###

To rebuild the css file after modification, download and install the [YUI Compressor](https://github.com/yui/yuicompressor), then run:

    java -jar yuicompressor.jar style.dev.css > style.css

*Yes, it requires [Java](http://java.com), but you may always just copy the style.dev.css to style.css and be done*

## License ##

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
