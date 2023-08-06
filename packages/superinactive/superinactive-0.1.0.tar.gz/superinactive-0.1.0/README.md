# superinactive
Supervisor plugin to monitor for file activity and restart program on inactivity

Imagine you have an infinite long running `ffmpeg` job, which converts a video stream on the fly.
After a certain time the file output does not change any more but supervisor does not detect the `ffmpeg` job as crashed.

This plugin may solve such situations.  

Installation:

    pip3 install superinactive

Configuration:

    [program:ffmpeg]
    command=ffmpeg ......  -o /home/volker/out.stream

    [program:superinactive]
    command=superinactive /home/volker/out.stream 10 ffmpeg

Command line options:

    usage: superinactive.py [-h] [-g GROUP] [-a] path timeout [prog [prog ...]]

    Supervisor plugin to monitor a file activity and restart programs on
    inactivity

    optional arguments:
      -h, --help            show this help message and exit

    file monitoring:
      path                  file path to monitor for inactivity
      timeout               timeout (seconds) for inactivity

    programs:
      prog                  supervisor program name to restart
      -g GROUP, --group GROUP
                            supervisor group name to restart
      -a, --any             restart any child of this supervisor
