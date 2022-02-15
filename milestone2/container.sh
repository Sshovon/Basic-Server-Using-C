#!/bin/bash

VARIABLE=$PWD/container 

if [ ! -d $VARIABLE ]; #checking if the path exists
then

    mkdir -p $VARIABLE/{bin,proc,etc,var/www,var/log,lib/x86_64-linux-gnu,lib64}  #creating directories

    cp /etc/mime.types $VARIABLE/var/www #copying mime.types into web root
    cp /home/frcs/vscode/c++/Assignment/server $VARIABLE/bin #copying server executable into container bin folder (change it)
    cp /home/frcs/Downloads/Group11/Group11/* $VARIABLE/var/www #copying html,css,images,xml to our web root (change it)

    cp  /lib/x86_64-linux-gnu/libc.so.6 $VARIABLE/lib/x86_64-linux-gnu  #copying dependent libraries necessary for executing server
    cp  /lib64/ld-linux-x86-64.so.2 $VARIABLE/lib64

    cd $VARIABLE/bin #changing path
    
    cp /bin/busybox . #copying busybox to our container bin folder
    
    touch $VARIABLE/var/log/debug.log #creating debug.log file

    for COMMAND in $(./busybox --list | grep -v busybox); #looping in busybox --list
    do
        ln busybox $COMMAND #hard linking busybox
    done
    #echo "::once:/bin/server" > $VARIABLE/etc/inittab #overriding init 
fi 

sudo VARIABLE=/bin unshare -pf --mount-proc /usr/sbin/chroot $VARIABLE /bin/sh #creating unshare container
#sudo VARIABLE=/bin unshare -pf --mount-proc /usr/sbin/chroot $VARIABLE /bin/init #creating unshare container and starting the server
