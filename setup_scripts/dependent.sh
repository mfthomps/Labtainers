#docker inspect --format='{{.Id}} {{.Parent}}' $(docker images --filter since=$1 -q) 
list=$(docker inspect --format='{{.Id}} {{.Parent}}' $(docker images --filter since=$1 -q) | awk '{print substr($1,8,12)}')
echo $list
docker rmi -f $list
