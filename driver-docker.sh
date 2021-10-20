# SET CONTEXT TO REMOTE HOST
docker context use $1

# RUN SIMULATION IN REMOTE HOST
docker run -d --name $2 manueldevillena/energy_community:v1_amd64

# COPY SIMULATION RESULTS
docker cp $2:/app/example/output results_docker/

# SET CONTEXT TO LOCAL HOST
docker context use default
