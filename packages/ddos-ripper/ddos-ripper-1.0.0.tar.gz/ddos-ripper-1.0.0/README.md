#### DDoS-Ripper

DDoS Ripper is a tool for testing if your web server is vulnerable to slow-requests kind of attacks.
A Distributable Denied-of-Service (DDOS) attack server that cuts off targets or surrounding infrastructure in a flood of Internet traffic

DDoS attacks achieve effectiveness using multiple compromised computer systems as a source of attack traffic.
Search engines may include computers and other network resources such as IoT devices.
From a higher level, the DDOS attack is like an unexpected traffic jam stuck on a highway, preventing regular traffic from reaching its destination.
The idea behind this approach to create as many connections with a server as possible and keep them alive and send trash headers through the connection.
Please DO NOT USE this in the real attacks on the servers. It's made for just testing purpose.
This tool not responsible for any abuse or damage caused by this program. Only for Educational Purpose.

More information about the attack you can find [here].

### Installation

#### PyPi

For installation through the PyPI:

```sh
$ pip install ddos-ripper==1.0.0
```
This method is prefered for installation of the most recent stable release.

#### Source-code

#### For Termux
To use the ddos-ripper type the following commands:

```sh
$pkg install git -y
$pkg install python -y
$pkg install python3 -y
$git clone https://github.com/palahsu/DDoS-Ripper.git
$cd DDoS-Ripper
$ls
$python3 DRipper.py 
$python3 DRipper.py -s [ip Address] -t 135
$python3 DRipper.py -s 0.00.00.00 -t 135
```

#### For Debian-based GNU/Linux distributions:
To use the application, type in the following commands in GNU/Linux terminal.

```sh
$sudo apt install git
$git clone https://github.com/palahsu/DDoS-Ripper.git
$cd DDoS-Ripper
$ls
$python3 DRipper.py` OR `python2 DRipper.py`
```

#### For Windows
To use the application, type in the following commands in Powershell or CMD:

```sh
$git clone https://github.com/palahsu/DDoS-Ripper
$cd DDoS-Ripper
$ls
$python3 DRipper.py` OR `python DRipper.py`
$python3 DRipper.py -s [ip Address] -t 135
$python3 DRipper.py -s 0.00.00.00 -t 135`
```

#### For MacOS

```sh
Install Brew and Install dependencies (python 3)
$python3 DRipper.py -s [ip Address] -t 135
$python3 DRipper.py -s 0.00.00.00 -t 135`
```
###### stop execution: Ctrl + C


### Bugs, issues and contributing!

If you find [bugs] or have [suggestions] about improving the module, don't hesitate to contact me.

### License

This project is licensed under the MPL License - see the [LICENSE](https://github.com/palahsu/DDoS-Ripper/blob/master/LICENSE) file for details.
Licenses may change in the future for version updates.
Copyright (c) 2019-2020 palahsu

[here]: <https://en.wikipedia.org/wiki/DDoS-Ripper_(computer_security)>
[bugs]: <https://github.com/palahsu/DDoS-Ripper/issues>
[suggestions]: <https://github.com/palahsu/DDoS-Ripper/issues>

