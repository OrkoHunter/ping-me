[![pypi version](https://img.shields.io/pypi/v/ping-me.svg)](https://github.com/OrkoHunter/ping-me/tree/v0.2)
[![Code Health](https://landscape.io/github/OrkoHunter/ping-me/master/landscape.svg?style=flat)](https://landscape.io/github/OrkoHunter/ping-me/master)
# ping-me
A Cross Platform personalized Ping

The beauty of `ping-me` is its command line interface. Get all of your
reminders done just by a single line command on your favorite terminal
screen. `ping-me` will *surely* ping you at that time, no matter you
are online or not. It will get to you on your phone device, smart watch
and even SMS in worst cases.

Stay Lazy, Stay Updated !

![alt text](bin/ping-me-e.png "ping-me -e")

## Project Status
 - [X] `ping-me` identifies date, time and message using flags
 - [X] `ping-me` asks for configuration on first request
 - [X] `ping-me` stores the configuration on remote server
 - [X] `ping-me` stores the message with datetime stamp on the server
 - [X] Server activates the ping 50 seconds prior to its exact time
 - [X] Server ready for a GET request
 - [ ] `ping-me` makes full use of natural language processing
 - [ ] `ping-me` notifies through chrome/firefox extension
 - [X] `ping-me` works on linux
 - [ ] `ping-me` works on windows
 - [ ] `ping-me` works on OS X
 - [ ] `ping-me` works on Android
 - [ ] `ping-me` sends texts to phone
 - [ ] `ping-me` ping-me works on ios
 - [ ] `ping-me` works on Windows phone


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
