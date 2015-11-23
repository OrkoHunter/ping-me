# ping-me
A Cross Platform personalized Ping

The beauty of `ping-me` is its command line interface. Get all of your
reminders done just by a single line command on your favorite terminal
screen. `ping-me` will *surely* ping you at that time, no matter you
are online or not. It will get to you on your phone device, smart watch
and even SMS in worst cases.

Stay Lazy, Stay Updated !

![alt text](bin/ping-me-e.png "ping-me -e")

## Installation

### From GitHub
```sh
$ pip install https://github.com/OrkoHunter/ping-me/archive/master.zip
```

__Using pip (To be done)__

__Using apt-get (To be done)__

## Usage

### Use of flags
```sh
$ ping-me -d November-24-2015 -t 14:30 Get up and eat!
```
By default `-d` and `-t` accounts for `datetime.today` and `00:00 hours`
respectively. Go ahead and make experiments with the syntax.

### No flags, pure language
```sh
$ ping-me to get up and eat tomorrow afternoon
```
