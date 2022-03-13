#!/bin/sh
echo "Content-type: text/plain; charset=utf-8"
echo ""


poems=`echo -n 'select * from poem;'  | sqlite3 /usr/local/apache2/DB/userDB.db -line`
echo $poems

IFS='= '
read -r -a arr <<< "$poems"

poemID=""
uid=""
poem=""
for i in "${!arr[@]}"
do 
    if [ "${arr[i]}" = "poemID" ]; then
        ((i=i+1))
        poemID=${arr[i]}
        poem=$(echo -n "select poem from poem where id=\"$poemID\" ;"  | sqlite3 /usr/local/apache2/DB/userDB.db -line)
        uid=$(echo -n "select uid from poem where id=\"$poemID\" ;"  | sqlite3 /usr/local/apache2/DB/userDB.db -line)
        echo "$poemID"
        echo "$poem"
        echo "$uid"
    fi

done



