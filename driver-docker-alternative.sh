#!/bin/zsh

if [[ -z $5 ]]; then
    echo -e "\nUsage:\n$0 arg1 arg2 arg3 arg4 arg5\n\narg1: docker context (point at host)\narg2: container name (to be set here)\narg3: volume name (to be set here)\narg4: output folder of the simulation results (host)\narg5: folder to copy the simulation results (local)"
exit
fi

# SET CONTEXT TO REMOTE HOST
docker context use $1

# RUN SIMULATION IN REMOTE HOST
docker run --name $2 -v $3:$4 sizing-merygrid-amd64

# CREATE DUMMY CONTAINER TO RETRIEVE RESULTS
docker run -d --name dummy.tmp -v $3:$4 python:3.7 sleep 1000

# COPY SIMULATION RESULTS
docker cp dummy.tmp:$4 $5

# REMOVE DUMMY CONTAINER
docker stop dummy.tmp
docker rm -f dummy.tmp

# SET CONTEXT TO LOCAL HOST
docker context use default

# EXAMPLES OF VARIABLES
# $1 = zeus
# $2 = container_energy_community
# $3 = volume_energy_community
# $4 = /app/example/output
# $5 = results_docker
