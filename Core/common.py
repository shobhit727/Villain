#
# Author: Panagiotis Chartas (t3l3machus) 
#
# This script is part of the "Villain C2 Framework": 
# https://github.com/t3l3machus/Villain


import base64
import os
import re
import socket
import string
import sys
from copy import deepcopy
from datetime import datetime
from ipaddress import ip_address
from platform import system as get_system_type
from secrets import choice
from typing import ClassVar
from uuid import UUID

import netifaces as ni
from Cryptodome.Cipher import AES

system_type = get_system_type()

# if system_type in ['Linux', 'Darwin']:
# 	import gnureadline as global_readline
# else:
import readline as global_readline

''' Colors '''
MAIN = '\001\033[38;5;85m\002'
GREEN = '\001\033[38;5;82m\002'
GRAY = PLOAD = '\001\033[38;5;246m\002'
NAME = '\001\033[38;5;228m\002'
RED = '\001\033[1;31m\002'
FAIL = '\001\033[1;91m\002'
ORANGE = '\001\033[0;38;5;214m\002'
LRED = '\001\033[0;38;5;196m\002'
BOLD = '\001\033[1m\002'
PURPLE = '\001\033[0;38;5;141m\002'
BLUE = '\001\033[0;38;5;12m\002'
UNDERLINE = '\001\033[4m\002'
UNSTABLE = '\001\033[5m\002'
END = '\001\033[0m\002'


''' MSG Prefixes '''
INFO = f'{MAIN}Info{END}'
WARN = f'{ORANGE}Warning{END}'
IMPORTANT = f'{ORANGE}Important{END}'
FAILED = f'{RED}Fail{END}'
ERR = f'{LRED}Error{END}'
DEBUG = f'{ORANGE}Debug{END}'
CHAT =f'{BLUE}Chat{END}'
GRN_BUL = f'[{GREEN}*{END}]'
ATT = f'{ORANGE}[!]{END}'
META = '[\001\033[38;5;93m\002M\001\033[38;5;129m\002e\001\033[38;5;165m\002t\001\033[38;5;201m\002a\001\033[0m\002]'

cwd = os.path.dirname(os.path.abspath(__file__))

''' Command Prompt Settings '''

class Main_prompt:
	
	original_prompt = prompt = f"{UNDERLINE}Villain{END} > "
	hoax_prompt = None
	ready = True
	SPACE = '#>SPACE$<#'
	exec_active = False

	
	@staticmethod
	def rst_prompt(prompt = prompt, prefix = '\r'):
		
		Main_prompt.ready = True
		Main_prompt.exec_active = False
		sys.stdout.write(prefix + Main_prompt.prompt + global_readline.get_line_buffer())


	@staticmethod
	def set_main_prompt_ready():
		Main_prompt.exec_active = False
		Main_prompt.ready = True



''' General Functions '''

def exit_with_msg(msg):
	print(f"[{DEBUG}] {msg}")
	sys.exit(0)



def print_fail_and_return_to_prompt(msg):			
	print(f'\r[{FAILED}] {msg}')
	Main_prompt.rst_prompt(force_rst = True)



def print_shadow(msg):
	print(f'{GRAY}{msg}{END}')



def print_debug(msg):
	print(f'\r[{DEBUG}] {msg}')



def do_nothing():
	pass



def get_datetime():
	date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	return date



def get_random_str(length):
	# choose from all lowercase letter
	chars = string.ascii_lowercase + string.digits
	rand_str = ''.join(choice(chars) for i in range(length))
	return rand_str


def get_file_contents(path, mode = 'rb'):

	try:
		with open(path, mode) as file_handle:
			return file_handle.read()

	except BaseException:  # noqa: BLE001
		return None



def is_valid_uuid(value):

	try:
		UUID(str(value))
		return True

	except BaseException:  # noqa: BLE001
		return False



def is_valid_ip(ip_addr):
	
	try:
		_ip_object = ip_address(ip_addr)
		return True
		
	except ValueError:
		return False



def parse_lhost(lhost_value):
	
	try:
		# Check if valid IP address
		lhost = str(ip_address(lhost_value))
		
	except ValueError:
		
		try:
			# Check if valid interface
			lhost = ni.ifaddresses(lhost_value)[ni.AF_INET][0]['addr']
			
		except BaseException:  # noqa: BLE001
			return False
	
	return lhost



def print_table(rows, columns):

	columns_list = [columns]
	
	for item in rows:

		# Values length adjustment
		try:
			for key in item:
				item_to_str = str(item[key])
				item[key] = item[key] if len(item_to_str) <= 20 else f"{item_to_str[0:8]}..{item_to_str[-8:]}"

		except BaseException:  # noqa: BLE001, S110
			pass

		columns_list.append([str(item[col] if item[col] is not None else '') for col in columns])
		
	col_size = [max(map(len, col)) for col in zip(*columns_list)]
	format_str = '  '.join([f"{{:<{i}}}" for i in col_size])
	columns_list.insert(1, ['-' * i for i in col_size])
	
	for item in columns_list:

		# Session Status ANSI
		item[-1] = f'{GREEN}{item[-1]}{END}' if item[-1] == 'Active' else item[-1]
		item[-1] = f'{ORANGE}{item[-1]}{END}' if (item[-1] in ['Unreachable', 'Undefined']) else item[-1]
		item[-1] = f'{LRED}{item[-1]}{END}' if (item[-1] in ['Lost']) else item[-1]

		# Stability ANSI
		item[-2] = f'{UNSTABLE}{item[-2]} {END}' if (columns_list[0][-2] == 'Stability' and item[-2] == 'Unstable') else item[-2]
		print(format_str.format(*item))



def clone_dict_keys(_dict):
	
	clone = deepcopy(_dict)
	clone_keys = clone.keys()
	return clone_keys



def get_terminal_columns():
    
	try:
		# Get the number of columns in the terminal
		columns = os.get_terminal_size().columns
		return columns
	
	except BaseException:  # noqa: BLE001
		# If there was an error, return a default value
		return 80 



def strip_ansi_codes(s):
    s = re.sub('\\[([0-9]+)(;[0-9]+)*m', '', s) 
    return re.sub('\033\\[([0-9]+)(;[0-9]+)*m', '', s) 



def clean_string(input_string):
	# Remove ANSI escape sequences
	ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
	input_string = ansi_escape.sub('', input_string)
	
	# Remove non-printable characters
	printable_chars = list(range(0x20, 0x7F)) + [0x09, 0x0A, 0x0D]
	input_string = ''.join(filter(lambda x: ord(x) in printable_chars, input_string))
	
	return input_string



def ansi_codes_detected(s):
    return bool(re.search('\x1b\\[([0-9]+)(;[0-9]+)*m', s) or re.search('\\[([0-9]+)(;[0-9]+)*m', s))



def match_regex(regex, data):

    match = regex.search(data)
    return bool(match)



def split_str_on_regex_index(regex, string):

	start_index = regex.search(string).start()
	return [string[0:start_index], string[start_index:]]



def check_list_for_duplicates(l):
	
	for elem in l:
		if l.count(elem) > 1:
			return True
			
	return False



def subtract_lists(l1, l2):
	
	set1 = set(l1)
	set2 = set(l2)
	
	result_set = set1 - set2
	result_list = list(result_set)
	
	return result_list



def print_columns(strings):
	if not strings:
		print(f'\r[{DEBUG}] No items to display. {strings}')
		return

	max_length = max(map(len, strings))
	column_width = max_length + 4
	column_count = max(1, min(len(strings), get_terminal_columns() // column_width))
	row_count = (len(strings) + column_count - 1) // column_count

	for row in range(row_count):
		row_items = []
		for column in range(column_count):
			index = column * row_count + row
			if index < len(strings):
				row_items.append(strings[index].ljust(column_width))
		print(''.join(row_items).rstrip())

	print("\n", end=" ")




class PrompHelp:
	
	deprecated: ClassVar[list] = ['exec']
	commands: ClassVar[dict] = {
	
		'connect' : {
			'details' : '''
Connect with another instance of Villain (sibling server). Once connected, you will be able to see and interact with foreign shell sessions owned by sibling servers and vice-versa. Multiple sibling servers can be connected at once. The limit of connections depends on the number of active threads a Villain instance can have (adjustable). In case you forgot the team server port number (default: 6501), use "sockets" to list Villain related services info. Read the Usage Guide or check my YouTube channel (@HaxorTechTones) for details.

connect <IP> <TEAM_SERVER_PORT>''',
			'least_args' : 2,
			'max_args' : 2
		},
				
				
		'generate' : {
			'details' : '''
Generate a reverse shell command. This function has been redesigned to use payload templates, which you can find in Villain/Core/payload_templates and edit or create your own.

Main logic:
generate payload=<OS_TYPE/HANDLER/PAYLOAD_TEMPLATE> lhost=<IP or INTERFACE> [ obfuscate encode ]

Handlers:
- reverse_tcp 
- hoaxshell

The "payload" argument supports tab-autocomplete, allowing for quick selection of valid OS types, handlers, and templates.

Usage examples:
generate payload=windows/reverse_tcp/powershell lhost=eth0 encode
generate payload=linux/hoaxshell/sh_curl lhost=eth0

- The ENCODE and OBFUSCATE attributes are enabled for certain templates and can be used during payload generation. 
- For info on a particular template, use "generate" with PAYLOAD being the only provided argument.
- To catch HoaxShell https-based reverse shells you need to start Villain with SSL.
- Ultimately, one should edit the templates and add obfuscated versions of the commands for AV evasion.''',
			'least_args' : 0, # Intentionally set to 0 so that the Payload_Generator class can inform users about missing arguments
			'max_args' : 7
		},			


		'exec' : {
			'details' : '''
Execute a command or file against an active shell session. Files are executed by being http requested from the Http File Smuggler. The feature works regardless if the session is owned by you or a sibling server.
	
exec <COMMAND or LOCAL FILE PATH> <SESSION ID or ALIAS>

*Command(s) should be quoted.''',
			'least_args' : 2,
			'max_args' : 2
		},			


		'inject' : {
			'details' : '''
Inject a local file using fileless execution over HTTP. The feature works regardless if the session is owned by you or a sibling server. 

From an active pseudo shell prompt:
inject <LOCAL FILE PATH> 

''',
			'least_args' : 1,
			'max_args' : 1,
			'shell' : True
		},		

		'repair' : {
			'details' : '''
Use this command to manually correct a shell session's hostname/username value, in case Villain does not interpret the information correctly when the session is established.
 	
repair <SESSION ID or ALIAS> <HOSTNAME or USERNAME> <NEW VALUE>''',
			'least_args' : 3,
			'max_args' : 3
		},	
			
		'shell' : {
			'details' : '''
Enables an interactive pseudo-shell prompt for a shell session. Press Ctrl+C to disable.
 
shell <SESSION ID or ALIAS>''',
			'least_args' : 1,
			'max_args' : 1
		},			

			
		'alias' : {
			'details' : '''
Set an alias for a shell session to use instead of session ID.

alias <ALIAS> <SESSION ID>''',
			'least_args' : 2,
			'max_args' : 2
		},			

			
		'reset' : {
			'details' : '''
Reset a given alias to the original session ID.

reset <ALIAS>''',
			'least_args' : 1,
			'max_args' : 1
		},			

		
		'kill' : {
			'details' : '''
Terminate a self-owned shell session.

kill <SESSION ID or ALIAS>''',
			'least_args' : 1,
			'max_args' : 1
		},		

		
		'help' : {
			'details' : '''Really?''',
			'least_args' : 0,
			'max_args' : 1
		},

		'siblings' : {
			'details' : '''
Print info about connected Sibling Servers. 
Siblings are basically other instances of Villain that you are connected with.''',
			'least_args' : 0,
			'max_args' : 0
		},

		'threads' : {
			'details' : '''
Villain creates a lot of threads to be able to handle multiple shell sessions, connections with siblings and more. In file Villain/Core/settings.py there is a BoundedSemaphore that works as a thread limiter to prevent resource contention, set by default to 100 (you can of course change it). This command lists the active threads created by Villain, to give you an idea of what is happening in the background, what is the current value of the thread limiter etc.
  
Note that, if the thread limiter reaches 0, weird things will start happening as new threads (e.g. shell sessions) will be queued until: thread limiter > 0.''',
			'least_args' : 0,
			'max_args' : 0
		},

		'sessions' : {
			'details' : '''Prints info about active shell shell sessions.''',
			'least_args' : 0,
			'max_args' : 0
		},

		'backdoors' : {
			'details' : '''Prints specifics about the shell and listener types of active shell shell sessions.''',
			'least_args' : 0,
			'max_args' : 0
		},

		'sockets' : {
			'details' : '''Prints Villain related socket services info.''',
			'least_args' : 0,
			'max_args' : 0
		},

		'id' : {
			'details' : '''Print server's unique ID.''',
			'least_args' : 0,
			'max_args' : 0
		},

		'upload' : {
			'details' : '''
Upload files into an active shell session over http (auto-requested from the http-file-smuggler service). The feature works regardless if the session is owned by you or a sibling server. 

From an active pseudo shell prompt:
upload <LOCAL_FILE_PATH> <REMOTE_FILE_PATH>''',
			'least_args' : 3,
			'max_args' : 3,
			'shell' : True
		},

		'cmdinspector' : {
			'details' : '''
Villain has a function that inspects user issued shell commands for input that may cause a shell shell session to hang (e.g., unclosed single/double quotes or backticks, commands that may start a new interactive session within the current shell and more). 
Use the cmdinspector command to turn that feature on/off. 

cmdinspector <ON / OFF>''',
			'least_args' : 1,
			'max_args' : 1
		},

		'conptyshell' : {
			'details' : '''
Automatically runs Invoke-ConPtyShell against a session. A new terminal window with netcat listening will pop up (you need to have gnome-terminal installed) and the script will be executed on the target as a new process, spawning a fully interactive shell. Currently works only for powershell.exe sessions.

Usage: 
conptyshell <IP or INTERFACE> <PORT> <SESSION ID or ALIAS>''',
			'least_args' : 3,
			'max_args' : 3
		},

		'exit' : {
			'details' : '''Kill all self-owned sessions and quit.''',
			'least_args' : 0,
			'max_args' : 0
		},

		'flee' : {
			'details' : '''Quit without terminating active sessions. When you start Villain again, if any HoaxShell implant is still running on previously injected hosts, the session(s) will be re-established.''',
			'least_args' : 0,
			'max_args' : 0
		},

		'clear' : {
			'details' : '''Come on man.''',
			'least_args' : 0,
			'max_args' : 0
		},

		'purge' : {
			'details' : '''Villain automatically stores information regarding generated implants and loads them in memory every time it starts. This way, HoaxShell generated implants become reusable and it is possible to re-establish older sessions, assuming the payload is still running on the victim(s). Use this command to delete all session related metadata. It does not affect any active sessions you may have.''',
			'least_args' : 0,
			'max_args' : 0
		},

		'redirectors' : {
			'details' : '''
Villain instances set traffic redirectors when using a shell session that belongs to a sibling. Use this command to list or remove redirectors, if required. 

Setting redirectors is handled automatically by Villain. Normally, users are not supposed to manually set redirectors. This feature exists purely for troubleshooting.

Usage: 
Type "redirectors" to list all active redirector entries.

To remove a redirector:
redirectors pop <REDIRECTOR ID>
''',
			'least_args' : 0,
			'max_args' : 2
		},
	}
	
	
	@staticmethod
	def print_main_help_msg():
				
		print(
		f'''
		\r  Main Prompt
		\r  -----------
		\r
		\r  Command              Description
		\r  -------              -----------
		\r  help         [+]     Print this message.
		\r  connect      [+]     Connect with a sibling server.
		\r  generate     [+]     Generate shell scripts.
		\r  siblings             Print sibling servers data table.
		\r  sessions             Print established shell sessions data table.
		\r  backdoors            Print established shell types data table.
		\r  sockets              Print Villain related running services' info.
		\r  redirectors  [+]     List and manage traffic redirectors.
		\r  shell        [+]     Enable an interactive pseudo-shell for a session.
		\r  alias        [+]     Set an alias for a shell session.
		\r  reset        [+]     Reset alias back to the session's unique ID.
		\r  kill         [+]     Terminate an established shell session.
		\r  conptyshell  [+]     Slap Invoke-ConPtyShell against a shell session.
		\r  repair       [+]     Manually correct a session's hostname/username info.
		\r  id                   Print server's unique ID (Self).
		\r  cmdinspector [+]     Turn Session Defender on/off.
		\r  threads              Print information regarding active threads.
		\r  clear                Clear screen.
		\r  purge                Delete all stored sessions metadata.
		\r  flee                 Quit without terminating active sessions.
		\r  exit                 Kill all sessions and quit.
		\r  
		\r
		\r  Pseudo Shell
		\r  ------------
		\r  
		\r  Command              Description
		\r  -------              -----------
		\r  upload       [+]     Upload files into an active shell session.
		\r  inject       [+]     Fileless exec of local scripts over http.
		\r
		\r  Commands starting with "#" are interpreted as messages and will be 
		\r  broadcasted to all connected Sibling Servers (chat).
		\r
        \r  Commands with [+] may require additional arguments.
        \r  For details use: {ORANGE}help <COMMAND>{END}
		''')
			


	@staticmethod
	def print_detailed(cmd):
		if cmd not in PrompHelp.deprecated:			
			PrompHelp.print_justified(PrompHelp.commands[cmd]['details'].strip()) if cmd in PrompHelp.commands \
			else print(f'No details for command "{cmd}".')
		else:
			print(f'The command "{cmd}" is deprecated.')


	@staticmethod
	def print_justified(text):
		
		text_length = len(text)
		text_lines = text.split('\n')
		wrapped_text = ''
		term_width = os.get_terminal_size().columns
		term_width_p = 100 if 100 <= (term_width) else term_width - 2
		
		if text_length >= term_width_p:
			
			lines = []
			
			for p in text_lines:
				
				if len(p) <= (term_width_p - 3):
					lines.append('  ' + p + ' ')
					continue

				words = p.split(' ')

				if words == ['']:
					continue

				else:					
					words_s = [w + ' ' for w in words]
					line_length = 0
					count = s = 0

					for w in words_s:
						
						line_length += len(w)

						if line_length < (term_width_p - 3):
							count += 1

						else:							
							lines.append('  ' + ' '.join(words[s:count]) + ' ')
							s = count
							count += 1
							line_length = len(w)
					
					if s < len(words):
						lines.append('  ' + ' '.join(words[s:]) + ' ')
				
			wrapped_text = '\n'.join(lines)

		else:
			wrapped_text = text
		
		print('\n' + wrapped_text, end='\n\n')



	@staticmethod
	def validate(cmd, num_of_args):
		
		valid = True
		
		if cmd not in PrompHelp.commands:
			print('Unknown command.')
			valid = False
		
		elif 'shell' in list(PrompHelp.commands[cmd].keys()):
			print(f'You need to be inside a pseudo shell session to use "{cmd}". Type "help {cmd}" for more info.')
			valid = False
			
		elif num_of_args < PrompHelp.commands[cmd]['least_args']:
			print('Missing arguments.')
			valid = False
		
		elif num_of_args > PrompHelp.commands[cmd]['max_args']:
			print('Too many arguments. Use "help <COMMAND>" for details.')
			valid = False			
	
		return valid



''' Shell Naming Conventions '''

bin2shell = {
	'powershell.exe' : 'PowerShell',
	'cmd.exe' : 'WIN_CMD',
	'unix' : 'Unix',
	'zsh' : 'Unix'
	}


bin2ext = {
	'powershell.exe' : '.ps1',
	'cmd.exe' : '.bat',
	'unix' : '.sh',
	'zsh' : '.sh'	
}


def multi_set(payload, set_dict):
	for key,val in set_dict.items():
		payload = payload.replace(key, str(val))
	return payload



def validate_host_address(addr):

	addr_verified = False
	try:
		# Check if valid IP address
		#re.search('[\d]{1,3}[\.][\d]{1,3}[\.][\d]{1,3}[\.][\d]{1,3}', lhost_value)
		addr_verified = str(ip_address(addr))

	except ValueError:

		try:
			# Check if valid interface
			addr_verified = ni.ifaddresses(addr)[ni.AF_INET][0]['addr']

		except BaseException:  # noqa: BLE001
			# Check if valid hostname
			if len(addr) > 255:
				addr_verified = False
				print('Hostname length greater than 255 characters.')
				return False
			
			if addr[-1] == ".":
				addr = addr[:-1]  # Strip trailing dot (used to indicate an absolute domain name and technically valid according to DNS standards)

			disallowed = re.compile(r"[^A-Z\d-]", re.IGNORECASE)
			if all(len(part) and not part.startswith("-") and not part.endswith("-") and not disallowed.search(part) for part in addr.split(".")):
				# Check if hostname is resolvable
				try:
					socket.gethostbyname(addr)
					addr_verified = addr
				
				except BaseException:  # noqa: BLE001
					print('Failed to resolve LHOST.')			
			
	return addr_verified



''' Encryption '''
def encrypt_msg(aes_key, msg, iv):
	enc_s = AES.new(aes_key, AES.MODE_CFB, iv)
	
	if type(msg) == bytes:
		cipher_text = enc_s.encrypt(msg)
	else:
		cipher_text = enc_s.encrypt(msg.encode('utf-8'))
		
	encoded_cipher_text = base64.b64encode(cipher_text)
	return encoded_cipher_text



def decrypt_msg(aes_key, cipher, iv):
	
	try:
		decryption_suite = AES.new(aes_key, AES.MODE_CFB, iv)
		plain_text = decryption_suite.decrypt(base64.b64decode(cipher + b'=='))
		return plain_text if type(plain_text) == str else plain_text.decode('utf-8', 'ignore')
	
	except TypeError:
		pass

