The skunky-hangprocessor project is a temporary solution for processing Firefox
hang reports until Socorro grows the necessary collection/query features. See
https://wiki.mozilla.org/Socorro/Hang_Processing_Proposal for the long-term 
proposal and motivation. See [Mozilla bug 784106](https://bugzilla.mozilla.org/show_bug.cgi?id=784106)
for deployment information.

This app is designed to handle low report volumes (1500 reports/day) and is
not intended to be scalable. That's what Socorro is for.

Typically the collector runs continuously (either directly from the command
line or as a WSGI app using fastcgi or mod_wsgi). A single instance of the
processor also runs on a cron job. The reporting is all flat files that can
be served directly. All data analysis will be done with some combination of
python and pig.

To get more information or help, please contact Benjamin Smedberg <benjamin@smedbergs.us>.

## Setup instructions

In `~/.bash_profile`, add: `export PYTHONPATH=$HOME/lib/python2.6/site-packages`

```
sudo yum install git
sudo yum install python-cherrypy
```

```
git clone https://github.com/mozilla/configman
cd configman && python setup.py install --prefix=~
```

```
mkdir ~/bin
```

Install minidump_stackwalk. Because I didn't want to install GCC and all the
necessary dev headers, I did this on another machine using static linking:

```
svn checkout http://google-breakpad.googlecode.com/svn/trunk/
CXXFLAGS='-static-libgcc -static-libstdc++ -static' ./configure && make
scp src/processor/minidump_stackwalk
```

I think that socorro already has a custom RPM for this, but I'm not sure.

```
mkdir ~/hangprocessor
git clone https://github.com/bsmedberg/skunky-hangprocessor ~/hangprocessor/code
```

```
mkdir ~/hangprocessor/data
mkdir ~/hangprocessor/queue
```


Write the following config file to `~/hangprocessor.ini`:

```
[top_level]
# collector_addr=0.0.0.0 Modify if binding to a particular address
collector_port=8000 # Pick the service port
collector_error_log = /home/bsmedberg/hangprocessor/collector.errors.log
collector_access_log = /home/bsmedberg/hangprocessor/collector.access.log
minidump_stackwalk_path=/home/bsmedberg/bin/minidump_stackwalk
minidump_storage_path=/home/bsmedberg/hangprocessor/data
symbol_paths=/mnt/netapp/breakpad/symbols_ffx:/mnt/netapp/breakpad/symbols_adobe:/mnt/netapp/breakpad/symbols_os
```

To launch the collector, run
```
nohup python ~/hangprocessor/code/hangprocessor/collector.py >/dev/null &
```

To launch the processor, run
```
nohup python -u ~/hangprocessor/code/hangprocessor/processor.py >> ~/hangprocessor/processor.log &
```
the -u forces logging to be immediate instead of buffered
