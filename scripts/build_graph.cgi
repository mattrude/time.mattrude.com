#!/usr/bin/rrdcgi
<HTML>
<HEAD><TITLE>RRDCGI Demo</TITLE></HEAD>
<BODY>
<H1>RRDCGI Example Page</H1>
<P>
<RRD::GRAPH Kirby-clients.png
--lazy
--imgformat=PNG
--start=-86400
--end=-300
--title='Kirby - 174.143.169.159 - Number of Active Clients'
--rigid
--height=120
--width=500
--alt-autoscale-max
--lower-limit=0
--vertical-label='Number of Clients'
--slope-mode
--font TITLE:12:
--font AXIS:8:
--font LEGEND:10:
--font UNIT:8:
DEF:a="/var/www/time.mattrude.com/rrd/kriby-client.rrd":clients:AVERAGE
DEF:b="/var/www/time.mattrude.com/rrd/kriby-client.rrd":abusive:AVERAGE
LINE:a#002A97FF:"Clients:" 
GPRINT:a:LAST:"Current\:%8.2lf %s" 
GPRINT:a:AVERAGE:"Average\:%8.2lf %s" 
GPRINT:a:MAX:"Maximum\:%8.2lf %s\n" 
AREA:b#F51D30FF:"Abusive:" 
GPRINT:b:LAST:" Current\:%8.2lf %s" 
GPRINT:b:AVERAGE:"Average\:%8.2lf %s" 
GPRINT:b:MAX:"Maximum\:%8.2lf %s\n"
>
</P>

<P>
<RRD::GRAPH Twyla-clients.png
--lazy
--imgformat=PNG
--start=-86400
--end=-300
--title='Twyla - 174.143.174.61 - Number of Active Clients'
--rigid
--height=120
--width=500
--alt-autoscale-max
--lower-limit=0
--vertical-label='Number of Clients'
--slope-mode
--font TITLE:12:
--font AXIS:8:
--font LEGEND:10:
--font UNIT:8:
DEF:a="/var/www/time.mattrude.com/rrd/twyla-client.rrd":clients:AVERAGE
DEF:b="/var/www/time.mattrude.com/rrd/twyla-client.rrd":abusive:AVERAGE
LINE:a#002A97FF:"Clients:" 
GPRINT:a:LAST:"Current\:%8.2lf %s" 
GPRINT:a:AVERAGE:"Average\:%8.2lf %s" 
GPRINT:a:MAX:"Maximum\:%8.2lf %s\n" 
AREA:b#F51D30FF:"Abusive:" 
GPRINT:b:LAST:" Current\:%8.2lf %s" 
GPRINT:b:AVERAGE:"Average\:%8.2lf %s" 
GPRINT:b:MAX:"Maximum\:%8.2lf %s\n">
</P>

<P>
<RRD::GRAPH samantha-clients.png
--lazy
--imgformat=PNG
--start=-86400
--end=-300
--title='Samantha - 174.143.173.49 - Number of Active Clients'
--rigid
--height=120
--width=500
--alt-autoscale-max
--lower-limit=0
--vertical-label='Number of Clients'
--slope-mode
--font TITLE:12:
--font AXIS:8:
--font LEGEND:10:
--font UNIT:8:
DEF:a="/var/www/time.mattrude.com/rrd/samantha-client.rrd":clients:AVERAGE
DEF:b="/var/www/time.mattrude.com/rrd/samantha-client.rrd":abusive:AVERAGE
LINE:a#002A97FF:"Clients:"
GPRINT:a:LAST:"Current\:%8.2lf %s"
GPRINT:a:AVERAGE:"Average\:%8.2lf %s"
GPRINT:a:MAX:"Maximum\:%8.2lf %s\n"
AREA:b#F51D30FF:"Abusive:"
GPRINT:b:LAST:" Current\:%8.2lf %s"
GPRINT:b:AVERAGE:"Average\:%8.2lf %s"
GPRINT:b:MAX:"Maximum\:%8.2lf %s\n">
</P>

</BODY>
</HTML>
