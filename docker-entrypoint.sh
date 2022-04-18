#!/bin/bash
echo "set vnc password as ${TASKID}"
/bin/bash -c "echo -e '${TASKID}\n${TASKID}\nn' | vncpasswd"; echo;
echo "start run jdlogin"
/usr/bin/vncserver -geometry 600x600 -fg -localhost no