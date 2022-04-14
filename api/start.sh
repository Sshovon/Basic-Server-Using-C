#!/bin/sh

#this is building custom image using Dockerfile
# -t --> name of image
docker build -t cgi-server-image .


#run will run the cgi-server-image to create a container
# --name --> name of container
# -p --> port of host:port of container
docker run --name cgiserver -p 8081:80 cgi-server-image

