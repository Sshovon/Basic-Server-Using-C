#!/bin/sh
echo "Content-type: text/html"

if [ "$REQUEST_METHOD" = "POST" ]; then
    if [ "$CONTENT_LENGTH" -gt 0 ]; then
        read -n $CONTENT_LENGTH POST_DATA <&0
        #echo "$CONTENT_LENGTH"
        uid=`echo "$POST_DATA" | awk '{split($0,array,"&")} END{print array[1]}' | awk '{split($0,array,"=")} END{print array[2]}'`
        password=`echo "$POST_DATA" | awk '{split($0,array,"&")} END{print array[2]}' | awk '{split($0,array,"=")} END{print array[2]}'`    
        hashed=$(echo -n $password | md5sum | awk '{print $1}')   
        user=$(echo -n "select uid from user where uid=\"$uid\" AND password=\"$hashed\"" |  sqlite3 /usr/local/apache2/DB/userDB.db )
    
    fi
  
fi

if [ ! -z "$user" ]    
then
 sessionID=$(echo -n "select sessionID from Session where uid=\"$user\";" |  sqlite3 /usr/local/apache2/DB/userDB.db)
 
 if [ -z "$sessionID" ]
 then
   sessionID=$(echo $RANDOM | md5sum | head -c 20)
   echo -e -n "INSERT INTO Session (\"sessionID\",\"uid\") VALUES (\"$sessionID\",\"$user\");" |  sqlite3 /usr/local/apache2/DB/userDB.db   
 fi

echo "Set-cookie:sessionID=$sessionID"
echo "Set-cookie:uid=$user"
   
fi

echo ""



if [  -z "$sessionID" ] 
then
    cat <<EOT
    <!DOCTYPE html>
    <html>
    <head>
            <title>Home</title>
    </head>
    <body>
        <h2>$HTTP_COOKIE</h2>
        <h3>Wrong Credentials, You won't be able to access all functionality.</h3>
        <h4>Register to get access.</h4>
        
    </body>
    </html>
EOT
else
    
    cat <<EOT
    <!DOCTYPE html>
    <html>
    <head>
            <title>Home</title>
    </head>
    <body>
        <h3>Welcome back, $user</h3>
        <h3>Welcome back, $HTTP_COOKIE</h3>
        
        <form action="/logout.cgi" me>
            <lable for="sessionID">SessionID</label>
            <input type="text" value="$sessionID" disabled/>
            <input type="submit" value="submit" />
        </form>


    </body>
    </html>
EOT
fi










