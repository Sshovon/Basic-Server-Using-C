#!/bin/sh

# Skriver ut 'http-header' for 'plain-text'
echo "Content-type:text/plain;charset=utf-8"

# Skriver ut tom linje for å skille hodet fra kroppen
echo


echo $REQUEST_URI 
echo $REQUEST_METHOD
echo

if [ "$REQUEST_METHOD" = "GET" ]; then
ID=$(echo $REQUEST_URI | grep -oP "(?<=\/other\/miljo\.sh\/poem\/)([0-9]+)$")
echo $ID
    
    if [ $REQUEST_URI == "/other/miljo.sh/logout/" ]; then
        echo "Du skal logge ut."
    elif [ $REQUEST_URI == "/other/miljo.sh/poem/" ]; then
        echo "Alle dikt skal hentes."
    #fi
    elif [ echo $REQUEST_URI | grep -q -oP "(?<=\/other\/miljo\.sh\/poem\/)([0-9]+)$" ]; then
        echo $REQUEST_URI | grep -oP "(?<=\/other\/miljo\.sh\/poem\/)([0-9]+)$"
        #echo Diktet $ID skal hentes.
    fi
fi

if [ "$REQUEST_METHOD" = "POST" ]; then
    echo Følgende skal settes inn i $REQUEST_URI:
    echo

    # skriver HTTP-hode
    head -c $CONTENT_LENGTH
    echo 
fi

if [ "$REQUEST_METHOD" = "PUT" ]; then
    echo $REQUEST_URI skal endres slik:
    echo

    # skriver-hode
    head -c $CONTENT_LENGTH
    echo 
fi

if [ "$REQUEST_METHOD" = "DELETE" ]; then
    echo $REQUEST_URI skal slettes
fi
