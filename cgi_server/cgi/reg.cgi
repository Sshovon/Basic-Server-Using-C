#!/bin/sh
echo "Content-type: text/html"
echo




if [ "$REQUEST_METHOD" = "POST" ]; then
    if [ "$CONTENT_LENGTH" -gt 0 ]; then
        read -n $CONTENT_LENGTH POST_DATA <&0
        #echo "$CONTENT_LENGTH"
        uid=`echo "$POST_DATA" | awk '{split($0,array,"&")} END{print array[1]}' | awk '{split($0,array,"=")} END{print array[2]}'`
        password=`echo "$POST_DATA" | awk '{split($0,array,"&")} END{print array[2]}' | awk '{split($0,array,"=")} END{print array[2]}'`    
        hashed=$(echo -n $password | md5sum | awk '{print $1}')
        echo -e -n "INSERT INTO User (\"uid\",\"password\") VALUES (\"$uid\",\"$hashed\");" |  sqlite3 /usr/local/apache2/DB/userDB.db   
    fi

fi

cat <<EOT
<!DOCTYPE html>
<html>
<head>
        <title>Welcome to our application</title>
</head>
<body>
       <h3>Registration Completed!!!</h3>
</body>
</html>
EOT




