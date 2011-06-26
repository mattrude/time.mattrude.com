#!/bin/sh

ROOT=/var/www/time.mattrude.com
POOLPAGE=$ROOT/status
TEMPLATESDIR=$ROOT/scripts/templates
DOCUMENTSDIR=$ROOT/documentation


### Building the README Page ###

cd $ROOT
rm -f $ROOT/readme.tmp $TEMPLATESDIR/readme.html
markdown $ROOT/README.md > $ROOT/readme.tmp
cat $TEMPLATESDIR/head > $DOCUMENTSDIR/readme.html
echo "                <div id="title">
                        <h1>time.mattrude.com <i>&mdash; Readme File</i></h1>
                </div>
                <p> <a href="/">time.mattrude.com</a> / <a href="/documentation/">documentation</a> / <strong>readme</strong> / </p>" >> $DOCUMENTSDIR/readme.html
cat $ROOT/readme.tmp $TEMPLATESDIR/tail >> $DOCUMENTSDIR/readme.html
rm -f $ROOT/readme.tmp

### Building per host cgi files ###

mkdir -p $ROOT/bin $ROOT/tmp
for X in `cat $ROOT/rrd/list-of-systems`
do
	rm -f $ROOT/bin/graphs-$X.cgi
        sed -e s/POOL/$X/g $TEMPLATESDIR/graphs.cgi > $ROOT/bin/graphs-$X.cgi
	chmod 755 $ROOT/bin/graphs-$X.cgi
done

### Building the Status Pages ###
mkdir -p $POOLPAGE
cd $POOLPAGE
cat /dev/null > out.template

echo "<h2>Time Server Hosts</h2>
<ul>" >> out.template
for X in `cat $ROOT/rrd/list-of-systems`
do
	echo "<li><a href=/status/$X/>$X</a>" >> out.template
done
echo "</ul>" >> out.template

for X in `cat /var/www/time.mattrude.com/rrd/list-of-systems`
do
	sed -e s/POOL/$X/g $TEMPLATESDIR/template >> out.template
done

sync
cat $TEMPLATESDIR/index-head out.template $TEMPLATESDIR/tail > $POOLPAGE/index.html

# Build the indexs for the hosts.
for X in `cat /var/www/time.mattrude.com/rrd/list-of-systems`
do
	mkdir -p $POOLPAGE/$X
	cat /dev/null > out.template
        sed -e s/POOL/$X/g $TEMPLATESDIR/template-host >> out.template
	sync
	cat out.template $TEMPLATESDIR/tail > $X/index.html
	rm -f out.template
	for a in clients offset jitter frequency sjit cjit wander disp
	do
		mkdir -p $POOLPAGE/$X/$a
		cat /dev/null > out.template
		sed -e s/POOL/$X/g $TEMPLATESDIR/template-by-type |sed -e s/TYPE/$a/g >> out.template
	        sync
	        cat out.template $TEMPLATESDIR/tail > $X/$a/index.html
	        rm -f out.template
	done
done
chown -R apache:apache $POOLPAGE
