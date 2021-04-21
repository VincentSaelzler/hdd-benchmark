# hdd-benchmark

## How to Run
Set up a client computer (usually using a live CD - I use Arch).
### Client
1.  Connect to network
1.  Get to a command line prompt
1.  Start ssh `systemctl start sshd.service`
1.  Set a PW `passwd`
1.  Detemine IP `ip address | grep 192`

### Server / Runner Setup and Config
1.  ssh into client `ssh root@[IP]`
1.  install git on client `pacman --sync --refresh git`
1.  clone this repo (use HTTPS) `git clone https://github.com/VincentSaelzler/hdd-benchmark.git`
1.  start `screen` (so the program runs even if SSH session is disconnected) 

### Running
#### Update Parameters
In `util.py` change `is_prod()` to return true.

**If you forget to do this, you will likely see output that looks like this. It will just go on forever.**
```
before dev sda
before smart FIRST sda
before match: /dev/sda - "in progress, 70% remaining"
in match: /dev/sda
Waiting for /dev/sda extended test to complete. 0.03333333333333333m of estimated 29m
post break: /dev/sda
```
In `main.py` ensure the device lists match the disks in your system. At time of writing, they are on lines 45 and 46.
```python
    dev_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    devs = [Dev('sd' + dl, now_unix) for dl in dev_letters]
```
This example is for 8 drives with the naming convention `sda`,`sdb`, ... `sdh`.

Also edit `main.py` to include an accurate description of the tests (optional). This is mainly useful if doing lots of tests with different sets of disks and/or test scenarios. At time of writing, this is on lines 14 and 15.

#### Run the Program
1.  **Required** change directory to root of git repo. Some relative file reference code is not robust.
1.  `cd hdd-benchmark`
1.  run the script `python3 main.py`
