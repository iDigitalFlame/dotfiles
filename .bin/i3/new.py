#!/usr/bin/python3
################################
###### iDigitalFlame 2018 ######
#                              #
#            -/`               #
#            -yy-   :/`        #
#         ./-shho`:so`         #
#    .:- /syhhhh//hhs` `-`     #
#   :ys-:shhhhhhshhhh.:o- `    #
#   /yhsoshhhhhhhhhhhyho`:/.   #
#   `:yhyshhhhhhhhhhhhhh+hd:   #
#     :yssyhhhhhyhhhhhhhhdd:   #
#    .:.oyshhhyyyhhhhhhddd:    #
#    :o+hhhhhyssyhhdddmmd-     #
#     .+yhhhhyssshdmmddo.      #
#       `///yyysshd++`         #
#                              #
########## SPACEPORT ###########
################################
## New Workspace
# iDigitalFlame 2018

from sys import exit
from json import loads, JSONDecodeError
from subprocess import Popen, PIPE, DEVNULL


def i3_command(i3_type):
    return i3_output(['-t', i3_type])


def i3_output(i3_command):
    i3_exec_params = i3_command
    if not isinstance(i3_command, list):
        i3_exec_params = str(i3_command).split(' ')
    try:
        i3_exec = Popen(['/usr/bin/i3-msg'] + i3_exec_params, stdout=PIPE, stderr=DEVNULL)
        if i3_exec.wait() != 0:
            print('[!] "i3-msg" returned non-zero status!')
            sys.exit(1)
        i3_output = i3_exec.stdout.read()
        if len(i3_output) > 0:
            try:
                i3_json = loads(i3_output.decode('UTF-8'))
                return i3_json
            except JSONDecodeError as err:
                print('[!] "i3-msg" output was not in JSON format! (%s)' % str(err))
                exit(1)
            except UnicodeDecodeError as err:
                print('[!] "i3-msg" could not be decoded! (%s)' % str(err))
                exit(1)
        return None
    except OSError as err:
        print('[!] Command to "i3-msg" failed! (%s)' % str(err))
        exit(1)


if __name__ == '__main__':
    i3_workspaces = i3_command('get_workspaces')
    if i3_workspaces is not None:
        i3_next_empty = next(x for x in range(1, 50) if not [w for w in i3_workspaces if w['num'] == x])
        i3_output(['workspace', 'number', str(i3_next_empty)])
        exit(0)
    exit(1)

# EOF