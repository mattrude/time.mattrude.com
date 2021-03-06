#!/usr/bin/perl -w

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# ntpgraphs -- a simple ntp graphing script
# mailgraph -- postfix mail traffic statistics
# copyright (c) 2011 Matt Rude <matt@mattrude.com>
# copyright (c) 2000-2007 ETH Zurich
# copyright (c) 2000-2007 David Schweikert <david@schweikert.ch>
# released under the GNU General Public License

use RRDs;
use POSIX qw(uname);

my $VERSION = "2.1";

my $host = 'POOL';
my $site = 'time.mattrude.com';
my $scriptname = 'graphs-POOL.cgi';
my $points_per_sample = 3;
my $xpoints = 650;
my $ypoints = 200;
my $ypoints_small = 111;
my $xpoints_small = 296;
my $rrd = '/var/www/time.mattrude.com/rrd/POOL.rrd'; # path to where the RRD database is
my $tmp_dir = '/var/tmp'; # temporary directory where to store the images

my @graphs = (
	{ title => 'Last Day',   seconds => 3600*24,        },
	{ title => 'Last Week',  seconds => 3600*24*7,      },
	{ title => 'Last Month', seconds => 3600*24*31,     },
	{ title => 'Last Year',  seconds => 3600*24*365, },
);

my %color = (
	sent     => '000099', # rrggbb in hex
	received => '009900',
	rejected => 'AA0000', 
	bounced  => '000000',
	virus    => 'DDBB00',
	spam     => '999999',
);

sub rrd_graph(@) {
	my ($range, $file, $ypoints, @rrdargs) = @_;
	my $step = $range*$points_per_sample/$xpoints;
	# choose carefully the end otherwise rrd will maybe pick the wrong RRA:
	my $end  = time; $end -= $end % $step;
	my $date = localtime(time);
	$date =~ s|:|\\:|g unless $RRDs::VERSION < 1.199908;

	my ($graphret,$xs,$ys) = RRDs::graph($file,
		'--imgformat', 'PNG',
		'--width', $xpoints,
		'--height', $ypoints,
		'--start', "-$range",
		'--end', $end,
		'--vertical-label', 'milliseconds',
		'--lower-limit', 0,
		'--units-exponent', 0, # don't show milli-messages/s
		'--lazy',
		'--color', 'SHADEA#ffffff',
		'--color', 'SHADEB#ffffff',
		'--color', 'BACK#ffffff',

		$RRDs::VERSION < 1.2002 ? () : ( '--slope-mode'),

		@rrdargs,

		'COMMENT:['.$date.']\r',
	);

	my $ERR=RRDs::error;
	die "ERROR: $ERR\n" if $ERR;
}

sub rrd_graph_small(@) {
        my ($range, $file, $ypoints_small, @rrdargs) = @_;
        my $step = $range*$points_per_sample/$xpoints;
        # choose carefully the end otherwise rrd will maybe pick the wrong RRA:
        my $end  = time; $end -= $end % $step;
        my $date = localtime(time);
        $date =~ s|:|\\:|g unless $RRDs::VERSION < 1.199908;

        my ($graphret,$xs,$ys) = RRDs::graph($file,
		'--title', 'POOL',
                '--imgformat', 'PNG',
                '--width', $xpoints_small,
                '--height', $ypoints_small,
                '--start', "-$range",
                '--end', $end,
                '--vertical-label', 'Number of Clients',
                '--lower-limit', 0,
                '--units-exponent', 0, # don't show milli-messages/s
                '--lazy',
                '--color', 'SHADEA#ffffff',
                '--color', 'SHADEB#ffffff',
                '--color', 'BACK#ffffff',

                $RRDs::VERSION < 1.2002 ? () : ( '--slope-mode'),

                @rrdargs,
        );

        my $ERR=RRDs::error;
        die "ERROR: $ERR\n" if $ERR;
}

sub graph_clients($$) {
        my ($range, $file) = @_;
        my $step = $range*$points_per_sample/$xpoints;
        rrd_graph($range, $file, $ypoints,
            "DEF:clients=$rrd:clients:LAST",
            "DEF:limited=$rrd:limited:LAST",
            "DEF:kod=$rrd:kod:LAST",
            'AREA:clients#002A97FF:Clients:',
            'GPRINT:clients:LAST:Current\:%8.3lf %s',
            'GPRINT:clients:AVERAGE:Average\:%8.3lf %s',
            'GPRINT:clients:MIN:Minimum\:%8.3lf %s',
            'GPRINT:clients:MAX:Maximum\:%8.3lf %s\n',
            'AREA:limited#ffff00:Limited:',
            'GPRINT:limited:LAST:Current\:%8.0lf %s',
            'GPRINT:limited:AVERAGE:Average\:%8.0lf %s',
            'GPRINT:limited:MIN:Minimum\:%8.0lf %s',
            'GPRINT:limited:MAX:Maximum\:%8.0lf %s\n',
            'AREA:kod#F51D30FF: K O D :',
            'GPRINT:kod:LAST:Current\:%8.0lf %s',
            'GPRINT:kod:AVERAGE:Average\:%8.0lf %s',
            'GPRINT:kod:MIN:Minimum\:%8.0lf %s',
            'GPRINT:kod:MAX:Maximum\:%8.0lf %s\n',
        );
}

sub graph_clients_small($$) {
        my ($range, $file) = @_;
        my $step = $range*$points_per_sample/$xpoints_small;
        rrd_graph_small($range, $file, $ypoints_small,
	    "DEF:clients=$rrd:clients:LAST",
            'AREA:clients#002A97FF: :',
            'GPRINT:clients:LAST:Now\:%8.2lf %s',
            'GPRINT:clients:AVERAGE:Avg\:%8.2lf %s',
            'GPRINT:clients:MAX:Max\:%8.2lf %s\n',
        );
}

sub graph_combo($$) {
        my ($range, $file) = @_;
        my $step = $range*$points_per_sample/$xpoints;
        rrd_graph($range, $file, $ypoints,
            "DEF:offset=$rrd:offset:LAST",
            'LINE1:offset#002A97FF:Offset:',
            'GPRINT:offset:LAST:Current\:%8.2lf %s',
            'GPRINT:offset:AVERAGE:Average\:%8.2lf %s',
            'GPRINT:offset:MIN:Minimum\:%8.2lf %s',
            'GPRINT:offset:MAX:Maximum\:%8.2lf %s\n',
            "DEF:cjit=$rrd:cjit:LAST",
            'LINE1:cjit#F51D30FF:cJit:',
            'GPRINT:cjit:LAST:Current\:%8.2lf %s',
            'GPRINT:cjit:AVERAGE:Average\:%8.2lf %s',
            'GPRINT:cjit:MIN:Minimum\:%8.2lf %s',
            'GPRINT:cjit:MAX:Maximum\:%8.2lf %s\n',
        );
}

sub graph_offset($$) {
        my ($range, $file) = @_;
        my $step = $range*$points_per_sample/$xpoints;
        rrd_graph($range, $file, $ypoints,
	    "DEF:offset=$rrd:offset:LAST",
	    'AREA:offset#002A97FF:Offset:',
	    'GPRINT:offset:LAST:Current\:%8.2lf %s',
            'GPRINT:offset:AVERAGE:Average\:%8.2lf %s',
            'GPRINT:offset:MIN:Minimum\:%8.2lf %s',
            'GPRINT:offset:MAX:Maximum\:%8.2lf %s\n',
        );
}

sub graph_sjit($$) {
        my ($range, $file) = @_;
        my $step = $range*$points_per_sample/$xpoints;
        rrd_graph($range, $file, $ypoints,
            "DEF:sjit=$rrd:sjit:LAST",
            'AREA:sjit#002A97FF:sJit:',
            'GPRINT:sjit:LAST:Current\:%8.2lf %s',
            'GPRINT:sjit:AVERAGE:Average\:%8.2lf %s',
            'GPRINT:sjit:MIN:Minimum\:%8.2lf %s',
            'GPRINT:sjit:MAX:Maximum\:%8.2lf %s\n',
        );
}

sub graph_cjit($$) {
        my ($range, $file) = @_;
        my $step = $range*$points_per_sample/$xpoints;
        rrd_graph($range, $file, $ypoints,
            "DEF:cjit=$rrd:cjit:LAST",
            'AREA:cjit#002A97FF:cJit:',
            'GPRINT:cjit:LAST:Current\:%8.2lf %s',
            'GPRINT:cjit:AVERAGE:Average\:%8.2lf %s',
            'GPRINT:cjit:MIN:Minimum\:%8.2lf %s',
            'GPRINT:cjit:MAX:Maximum\:%8.2lf %s\n',
        );
}

sub graph_wander($$) {
        my ($range, $file) = @_;
        my $step = $range*$points_per_sample/$xpoints;
        rrd_graph($range, $file, $ypoints,
            "DEF:wander=$rrd:wander:LAST",
            'AREA:wander#002A97FF:Wander:',
            'GPRINT:wander:LAST:Current\:%8.2lf %s',
            'GPRINT:wander:AVERAGE:Average\:%8.2lf %s',
            'GPRINT:wander:MIN:Minimum\:%8.2lf %s',
            'GPRINT:wander:MAX:Maximum\:%8.2lf %s\n',
        );
}

sub graph_freq($$) {
        my ($range, $file) = @_;
        my $step = $range*$points_per_sample/$xpoints;
        rrd_graph($range, $file, $ypoints,
            "DEF:freq=$rrd:freq:LAST",
            'AREA:freq#002A97FF:Freq:',
            'GPRINT:freq:LAST:Current\:%8.2lf %s',
            'GPRINT:freq:AVERAGE:Average\:%8.2lf %s',
            'GPRINT:freq:MIN:Minimum\:%8.2lf %s',
            'GPRINT:freq:MAX:Maximum\:%8.2lf %s\n',
        );
}

sub graph_disp($$) {
        my ($range, $file) = @_;
        my $step = $range*$points_per_sample/$xpoints;
        rrd_graph($range, $file, $ypoints,
            "DEF:disp=$rrd:disp:LAST",
            'AREA:disp#002A97FF:Disp:',
            'GPRINT:disp:LAST:Current\:%8.2lf %s',
            'GPRINT:disp:AVERAGE:Average\:%8.2lf %s',
            'GPRINT:disp:MIN:Minimum\:%8.2lf %s',
            'GPRINT:disp:MAX:Maximum\:%8.2lf %s\n',
        );
}

sub print_html()
{
	print "Content-Type: text/html\n\n";

	print <<HEADER;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>$site :: $host Time Server Status Page</title>
<meta http-equiv="Refresh" content="300" />
<meta http-equiv="Pragma" content="no-cache" />
<link rel="stylesheet" type="text/css" href="/style.css" />
</head>
<body>
<div id="content"> 
	<div id="primary" class="main"> 
HEADER

	print "<div id='title'><h1>$site <i>&mdash; $host Server Status</i></h1></div>\n";

	print "<ul id=\"jump\">\n";
	for my $n (0..$#graphs) {
		print "  <li><a href=\"#G$n\">$graphs[$n]{title}</a>&nbsp;</li>\n";
	}
	print "</ul>\n";

	for my $n (0..$#graphs) {
		print "<h2 id=\"G$n\">$graphs[$n]{title}</h2>\n";
		print "<div class='center'><p><img src=\"$scriptname?${n}-clients\" alt=\"NTP Graph, Clients\"/><br/>\n";
		print "<img src=\"$scriptname?${n}-offset\" alt=\"NTP Graph, Offset\"/><br/>\n";
		print "<img src=\"$scriptname?${n}-freq\" alt=\"NTP Graph, Freq\"/><br/>\n";
		print "<img src=\"$scriptname?${n}-sjit\" alt=\"NTP Graph, sJit\"/><br/>\n";
		print "<img src=\"$scriptname?${n}-cjit\" alt=\"NTP Graph, cJit\"/><br/>\n";
		print "<img src=\"$scriptname?${n}-wander\" alt=\"NTP Graph, Wander\"/><br/>\n";
		print "<img src=\"$scriptname?${n}-disp\" alt=\"NTP Graph, Disp\"/></p></div>\n";
	}

	print <<FOOTER;
</div> 
	<div id="footer"> 
	    <div class="footer-left"> 
		<p><a href='http://time.mattrude.com'>Home</a> | <a href='/status/'>Status</a> | <a href='/documentation/'>Documentation</a> | <a href='https://github.com/mattrude/time.mattrude.com'>Source</a></p> 
	    </div> 
	    <div class="footer-right"> 
		<p>Copyright &copy; 2009 &mdash; 2011 by <a href='http://mattrude.com'>Matt Rude</a></p> 
	    </div> 
	</div> 
</div> 
</body></html>
FOOTER
}

sub send_image($)
{
	my ($file)= @_;

	-r $file or do {
		print "Content-type: text/plain\n\nERROR: can't find $file\n";
		exit 1;
	};

	print "Content-type: image/png\n";
	print "Content-length: ".((stat($file))[7])."\n";
	print "\n";
	open(IMG, $file) or die;
	my $data;
	print $data while read(IMG, $data, 16384)>0;
}

sub main()
{
	mkdir $tmp_dir, 0777 unless -d $tmp_dir;
	mkdir "$tmp_dir", 0777 unless -d "$tmp_dir";
	mkdir "$tmp_dir/$host", 0777 unless -d "$tmp_dir/$host";

	my $img = $ENV{QUERY_STRING};
	if(defined $img and $img =~ /\S/) {
                if($img =~ /^(\d+)-clients$/) {
                        my $file = "$tmp_dir/$host/ntpgraph_$1_clients.png";
                        graph_clients($graphs[$1]{seconds}, $file);
                        send_image($file);
                } elsif($img =~ /^(\d+)-clients-small$/) {
                        my $file = "$tmp_dir/$host/ntpgraph_$1_clients-small.png";
                        graph_clients_small($graphs[$1]{seconds}, $file);
                        send_image($file);
                } elsif($img =~ /^(\d+)-offset$/) {
                        my $file = "$tmp_dir/$host/ntpgraph_$1_offset.png";
                        graph_offset($graphs[$1]{seconds}, $file);
                        send_image($file);
                } elsif($img =~ /^(\d+)-combo$/) {
                        my $file = "$tmp_dir/$host/ntpgraph_$1_combo.png";
                        graph_combo($graphs[$1]{seconds}, $file);
                        send_image($file);
                } elsif($img =~ /^(\d+)-sjit$/) {
                        my $file = "$tmp_dir/$host/ntpgraph_$1_sjit.png";
                        graph_sjit($graphs[$1]{seconds}, $file);
                        send_image($file);
                } elsif($img =~ /^(\d+)-cjit$/) {
                        my $file = "$tmp_dir/$host/ntpgraph_$1_cjit.png";
                        graph_cjit($graphs[$1]{seconds}, $file);
                        send_image($file);
                } elsif($img =~ /^(\d+)-wander$/) {
                        my $file = "$tmp_dir/$host/ntpgraph_$1_wander.png";
                        graph_wander($graphs[$1]{seconds}, $file);
                        send_image($file);
                } elsif($img =~ /^(\d+)-freq$/) {
                        my $file = "$tmp_dir/$host/ntpgraph_$1_freq.png";
                        graph_freq($graphs[$1]{seconds}, $file);
                        send_image($file);
                } elsif($img =~ /^(\d+)-disp$/) {
                        my $file = "$tmp_dir/$host/ntpgraph_$1_disp.png";
                        graph_disp($graphs[$1]{seconds}, $file);
                        send_image($file);
                } else {
			die "ERROR: invalid argument\n";
		}
	}
	else {
		print_html;
	}
}

main;
