#!/bin/sh

#header starts

echo "Content-type: text/html"

#retrives data from login form.
if [ "$REQUEST_METHOD" = "POST" ]; then
    if [ "$CONTENT_LENGTH" -gt 0 ]; then
        read -n $CONTENT_LENGTH POST_DATA <&0
        #echo "$CONTENT_LENGTH"
        uid=`echo "$POST_DATA" | awk '{split($0,array,"&")} END{print array[1]}' | awk '{split($0,array,"=")} END{print array[2]}'` #retriving the uid
        password=`echo "$POST_DATA" | awk '{split($0,array,"&")} END{print array[2]}' | awk '{split($0,array,"=")} END{print array[2]}'`   #retriving the password
        hashed=$(echo -n $password | md5sum | awk '{print $1}')   # creating a hash again so that we can compare / check it from our database
        # searching uid and password from our database 
        user=$(echo -n "select uid from user where uid=\"$uid\" AND password=\"$hashed\"" |  sqlite3 /usr/local/apache2/DB/userDB.db )
    
    fi
  
fi

# 3 case for generating sessionID
# case 1: you are a valid user and you are already logged in --> extract the stored sessionID and use it
# case 2: you are a valid user and you are not logged in --> generate a sessionID and store it in the database
# case 3: you are a invalid user --> wrong credentials page



if [ ! -z "$user" ]    #if you are a valid user 
then # if you are valid then
 sessionID=$(echo -n "select sessionID from Session where uid=\"$user\";" |  sqlite3 /usr/local/apache2/DB/userDB.db) # checking if you have any saved sessionID in the database
 
 if [ -z "$sessionID" ] # if you have sessionID in database?
 then # if you dont have any sessionID stored that means you are not logged in and we need to generate a sessionID
   sessionID=$(echo $RANDOM | md5sum | head -c 20)  #generating session id from hash of random number and taking the first 20 character
   #storing sessionID in database
   echo -e -n "INSERT INTO Session (\"sessionID\",\"uid\") VALUES (\"$sessionID\",\"$user\");" |  sqlite3 /usr/local/apache2/DB/userDB.db   
 fi
# $user means uid
echo "Set-cookie:sessionID=$sessionID"
echo "Set-cookie:uid=$user"
echo  "Set-cookie:status=1"
fi

#this empty echo means end of the header
echo ""

#header ends

if [  -z "$sessionID" ]  # checking if sesssionID is empty or not
then # if  empty then it means you are  invalid and we will give you the wrong credential page
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
else # you are valid user and we give you the homepage
    
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










