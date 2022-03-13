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
echo  "Set-cookie:status=1"
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

         <form action="post_poem.cgi" method="post">
                <label>Poem Name</label>
                <input type="text" name="pname">
                <br>
                <button type="submit">Add Poem</button>
        </form>
        <br><br><br>
         <form action="get_poem_by_id.cgi" method="get">
                <label>Poem ID</label>
                <input type="text" name="pid">
                <br>
                <button type="submit">Search</button>
        </form>
        <br><br><br>
        <form action="get_own_poems.cgi" method="get">
                <button type="submit">Own Poems</button>
        </form>
        <br><br><br>
        <form action="get_all_poems.cgi" method="get">
                <button type="submit">All Poems</button>
        </form>
        <br><br><br>
        <br><br><br>
        <form action="/logout.cgi">
            <input type="submit" value="LOGOUT" />
        </form>


    </body>
    </html>
EOT
fi










