#!/bin/sh

osascript -e 'tell app "Terminal"
    do script "cd GitHub/RemoteAccessTool/src; python3 attacker_main.py"
end tell'


sleep 1

osascript -e 'tell app "Terminal"
    do script "cd GitHub/RemoteAccessTool/src; python3 victim_main.py"
end tell'

