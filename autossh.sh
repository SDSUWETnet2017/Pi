#!/bin/bash

konsole --noclose -e sshpass -p "o3RteIip" ssh -R 19999:localhost:22 -o "ServerAliveInterval 20" -o "ServerAliveCountMax 3" wetnet@volta.sdsu.edu
