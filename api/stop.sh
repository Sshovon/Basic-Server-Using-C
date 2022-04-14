#!/bin/bash

#stop is like a pause --> after stop you can resume again from the previously saved state
docker stop cgiserver


#rm is remove the container totally
docker rm cgiserver
