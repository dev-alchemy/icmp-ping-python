The following code is tested on the following environment :
1. Programming Language : Python v3.8
2. Operating System Environment : MacOS Monterey 12.2
    sysname='Darwin', 
    nodename='potatoHunter.local', 
    release='21.3.0', 
    version='Darwin Kernel Version 21.3.0: Wed Jan  5 21:37:58 PST 2022; 
    root:xnu-8019.80.24~20/RELEASE_X86_64', machine='x86_64') **

(** This information is for information only please don't use this information for any other activity)

Run the following commands (sudo is admin privileges in linux and unix based OS):
    For pinging a local receiver
        - sudo python reciever.py
        - sudo python main.py 127.0.0.1

    For pinging a public network 
        - sudo python main.py <FULL_PUBLIC_DOMAIN e.g www.google.com>

Run the following command on windows (Untested)
    For pinging a local receiver
        - python reciever.py
        - python main.py 127.0.0.1

    For pinging a public network 
        - python main.py <FULL_PUBLIC_DOMAIN e.g www.google.com>

Remember to exit the receiver with CTRL+Z or CTRL+X once the results are obtained otherwise it will keep using resources
