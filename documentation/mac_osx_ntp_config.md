It.s been a while. Here is a simple guide in setting up an NTP Server in your Mac OS X. Although it does look trivial, it took me a while to figure it out (and find solutions out there). Steps 1 & 2 are important, as it does the trick.

* Disable the synchronizing of the local clock to ntp. Uncheck .Set date & time automatically..
* If you find NTP in the services offered in Server Admin, stop it also.
* Open the Terminal. Create or edit /etc/ntp.conf and add the ntp servers from where you will synch.
    server 0.asia.pool.ntp.org minpoll 12 maxpoll 17
    server 1.asia.pool.ntp.org minpoll 12 maxpoll 17
    server 2.asia.pool.ntp.org minpoll 12 maxpoll 17
    server 3.asia.pool.ntp.org minpoll 12 maxpoll 17
    server 0.jp.pool.ntp.org minpoll 12 maxpoll 17

* Edit or check /etc/ntp-restrict.conf. Add the allowed ip address range to synch with your server.
    restrict 10.0.0.0 mask 255.0.0.0 nomodify notrap
    restrict 202.92.128.0 mask 255.255.224.0 nomodify notrap

* Edit /etc/hostconfig.
    TIMESYNC=-NO-
    TIMESERV=-YES-

* Reboot server.
* Check if process is running: ps ax| grep ntp
* Check if it is synching with external ntp servers: ntpq -p
