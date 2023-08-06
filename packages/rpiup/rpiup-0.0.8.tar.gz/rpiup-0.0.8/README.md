# rpiup - Raspberry Pi OS Setup

## Install

```bash
pip install rpiup
```

## Usage

### Initializing an application
This is one time setup that you should only need to run once for each application.
##### download the latest Raspberry OS (firstboot)
The OS is from https://github.com/nmcclain/raspberian-firstboot
This is a modified RPi OS where the only change is that it lets you run a script on first boot.
```bash
rpiup os download
```

##### Initialize your application files
This creates a directory and copies the default files into it. If `./sd` is omitted, it will use the current directory (`./`).

The files in this directory will all be copied into the raspberry pi boot directory after it is flashed.
```bash
rpiup init ./myapp
# whats the app name? ...
# What should the device username be? ...
# What should the device password be? ...
# Do you want to set a git username?
# Do you want to set a git password?
# what's your wifi?: ...
# Do you have a set of alternate wifi credentials you would like to add?
# any app variables you want to set? (press enter to skip) ...
# all set!
cd myapp
ls *
# firstboot.sh
#
# resources:
# aps.yml docker services setup.sh vars.sh
```

#### Install Balena Etcher
This is an application that will flash your OS image onto your SD card. You can find it [here](https://www.balena.io/etcher/).

### Device Specific Setup
Repeat for each device you want to setup.

##### Flash your SD Card
 - Insert your SD card
 - Open Etcher and flash the downloaded os image (should be in the directory above `myapp/`)

##### Copy files over and finish device specific configuration
```bash
rpi sd setup
# by default, the hostname will be <APP_NAME>-<ETH0_MAC_ADDR>
# but you can set a custom hostname
rpi sd setup --hostname mytestpi
```
###### Alternatives

If you're doing a large batch of devices, it can make sense to generate the hostnames before and print out a list of labels to put on the devices. To do that:
```bash
### Run once - generate the hostname list and save it to a tsv file:
# pip install randomname
randomname saved --name myapp -g myapp,uuid/8 -n 100 --overwrite

randomname saved --name myapp export > hostnames.tsv

### Run for each device:
# increment the index at the end of the line
rpi sd setup --hostname $(randomname saved --name myapp get 0)
# increment from 0 to 1
rpi sd setup --hostname $(randomname saved --name myapp get 1)
# and so on...
```

## What it can do:
 - set the device hostname
 - set wifi networks
 - set arbitrary variables that can be accessed from the device.
 - run arbitrary commands


### CLI

#### Set the hostname
```bash
rpiup vars set --hostname blah-091091eh901eh
# or
pip install randomname
rpiup vars set --hostname $(randomname get)
```

##### Setting arbitrary environment variables
```bash
rpiup vars set --some-feature 1 --myapp_something blah
```

#### Set wifi networks
```bash
rpiup wifi add MySSID-2G
# enter password:

# or
rpiup wifi add MySSID-2G mypassword
```
