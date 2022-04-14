#!/bin/sh
echo "Content-type: text/html"
echo 



if [ "$REQUEST_METHOD" = "POST" ]; then
    if [ "$CONTENT_LENGTH" -gt 0 ]; then
        read -n $CONTENT_LENGTH POST_DATA <&0 #reading data provided by html form post method
        #echo "$CONTENT_LENGTH"
        uid=`echo "$POST_DATA" | awk '{split($0,array,"&")} END{print array[1]}' | awk '{split($0,array,"=")} END{print array[2]}'`  #retriving uid / email
        password=`echo "$POST_DATA" | awk '{split($0,array,"&")} END{print array[2]}' | awk '{split($0,array,"=")} END{print array[2]}'` # retriving password
        fname=`echo "$POST_DATA" | awk '{split($0,array,"&")} END{print array[3]}' | awk '{split($0,array,"=")} END{print array[2]}'`  #retriving first name
        lname=`echo "$POST_DATA" | awk '{split($0,array,"&")} END{print array[4]}' | awk '{split($0,array,"=")} END{print array[2]}'`    #retiving last name
        hashed=$(echo -n $password | md5sum | awk '{print $1}') #using md5sum hasing algorithm to create hash of password and awk to remove trailing space and -
        
        #storing user information in sqlite database
        echo -e -n "INSERT INTO User (\"uid\",\"password\",\"fname\",\"lname\") VALUES (\"$uid\",\"$hashed\",\"$fname\",\"$lname\");" |  sqlite3 /usr/local/apache2/DB/userDB.db   
        
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




