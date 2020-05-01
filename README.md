# hdd-benchmark

## How to Run
Set up a client computer (usually using a live CD - I use Arch).
### Client
1.  Connect to network
1.  Get to a command line prompt
1.  Start ssh `systemctl start openssh`
1.  Set a PW `passwd`
1.  Detemine IP `ip address`

### Server / Runner Setup and Config
1.  ssh into client `ssh root@[IP]`
1.  install git on client `pacman -Syu git`
1.  clone this repo (use HTTPS) `git clone https://github.com/VincentSaelzler/hdd-benchmark.git`
1.  edit main.py to include correct device letters, and a description of the tests. `nano hdd-benchmark/main.py`

### Running
1.  **Required** change directory to root of git repo. Some relative file reference code is not robust.
1.  `cd hdd-benchmark`
1.  run the script `python3 main.py`
