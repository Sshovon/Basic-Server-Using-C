#!/bin/bash

if [ "$REQUEST_METHOD" = "POST" ] || [ "$REQUEST_METHOD" = "DELETE" ] || [ "$REQUEST_METHOD" = "PUT" ]; then
        if [ "$CONTENT_LENGTH" -gt 0 ]; then
                read -n $CONTENT_LENGTH BODY_RES <&0
        fi
fi



sessionID=`echo $HTTP_COOKIE | awk '{split($0,array,";")} END{print array[1]}' | awk '{split($0,array,"=")} END{print array[2]}'`
email=`echo $HTTP_COOKIE | awk '{split($0,array,";")} END{print array[2]}' | awk '{split($0,array,"=")} END{print array[2]}'`
echo "Set-cookie:sessionID=$sessionID"
echo "Set-cookie:uid=$email"


#echo "Content-type:text/plain;charset=utf-8"
echo "Content-type:application/xml;charset=utf-8"


echo ""


# echo $BODY_RES
# echo $HTTP_COOKIE
# echo $REQUEST_URI

if [ "$REQUEST_METHOD" = "POST" ];then

    if [ $REQUEST_URI = '/login' ];then
        email=`echo $BODY_RES | awk -F '<email>'  '{print $2}' | awk -F '</email>' '{print $1}'`
        password=`echo $BODY_RES | awk -F '<password>'  '{print $2}' | awk -F '</password>' '{print $1}'`
        hashed=$(echo -n $password | md5sum | awk '{print $1}')
        user=$(echo -n "select email from user where email=\"$email\" AND password=\"$hashed\"" |  sqlite3 /usr/local/apache2/DB/userDB.db )
        # echo $email
        # echo $password
        # echo $user
        
        if [ ! -z $user ];then
            sessionID=$(echo $RANDOM | md5sum | head -c 20)
            echo -e -n "INSERT INTO Session (\"sessionID\",\"email\") VALUES (\"$sessionID\",\"$user\");" |  sqlite3 /usr/local/apache2/DB/userDB.db  
            echo "<Response><message>Succeful</message><sessionID>$sessionID</sessionID></Response>"
        else
            echo "<Response><message>Invaild credentails</message></Response>"
        fi
     
    
    fi

    if [ $REQUEST_URI = '/poem' ];then
        if [ ! -z $sessionID ];then
            email=$(echo -n "select email from Session where sessionID=\"$sessionID\"" |  sqlite3 /usr/local/apache2/DB/userDB.db )
            #echo $email
            poem=`echo $BODY_RES | awk -F '<title>'  '{print $2}' | awk -F '</title>' '{print $1}'`
            #echo $poem
            echo -n "INSERT INTO Poem (poem, email) VALUES (\"$poem\",\"$email\" );" | sqlite3 /usr/local/apache2/DB/userDB.db
            echo "<Response><message>Poem added!</message></Response>"
            
        else
            echo "<Response><message>You are not logged in!!</message></Response>"
        fi
    

    fi



fi

if [ "$REQUEST_METHOD" = "GET" ];then

    if [ $REQUEST_URI = '/logout' ];then
        #echo $HTTP_COOKIE
        sessionID=`echo $HTTP_COOKIE | awk '{split($0,array,";")} END{print array[1]}' | awk '{split($0,array,"=")} END{print array[2]}'`
        echo -e -n "DELETE FROM Session WHERE sessionID = \"$sessionID\" ;" |  sqlite3 /usr/local/apache2/DB/userDB.db
        echo "<Response><message>Logout Successful</message></Response>"
    fi

    if [ $REQUEST_URI = '/poems' ];then
        
        echo  "<Poems>"
        poems=$(echo "select poemID from poem;" | sqlite3 /usr/local/apache2/DB/userDB.db)
        poems=$(echo $poems)
        IFS=" "
        read -ra arr <<< "$poems"

        for element in "${arr[@]}"
        do 
        #we also have to search email based on poemID 
        email=$(echo -n "select email from poem where poemID=\"$element\";" |  sqlite3 /usr/local/apache2/DB/userDB.db)
        poem=$(echo -n "select poem from poem where poemID=\"$element\";" |  sqlite3 /usr/local/apache2/DB/userDB.db)
        cat <<EOF
        <Poem> 
            <PoemID> $element </PoemID> 
            <PoemName> $poem </PoemName> 
            <email> $email </email> 
        </Poem>
EOF
        done

        echo "</Poems>"
    
    fi


    if [[ $REQUEST_URI =~ ^/(poem)+/[^/]*[0-9]$ ]];then
        poemID=`echo $REQUEST_URI | cut -d '/' -f 3`  
        email=$(echo -n "select email from poem where poemID=\"$poemID\";" |  sqlite3 /usr/local/apache2/DB/userDB.db)
        poem=$(echo -n "select poem from poem where poemID=\"$poemID\";" |  sqlite3 /usr/local/apache2/DB/userDB.db)
        cat <<EOF
        <Poem> 
            <PoemID> $poemID </PoemID> 
            <PoemName> $poem </PoemName> 
            <email> $email </email> 
         </Poem>
EOF
    fi


    if [ $REQUEST_URI = '/poems/own' ];then
        email=$(echo -n "select email from Session where sessionID=\"$sessionID\"" |  sqlite3 /usr/local/apache2/DB/userDB.db )
        poems=$(echo "select poemID from poem where email=\"$email\";" | sqlite3 /usr/local/apache2/DB/userDB.db)
        poems=$(echo $poems)
        IFS=" "
        read -ra arr <<< "$poems"
        echo "<Poems>"
        for element in "${arr[@]}"
        do 
            poem=$(echo -n "select poem from poem where poemID=\"$element\";" |  sqlite3 /usr/local/apache2/DB/userDB.db)
        cat <<EOF
        <Poem>
            <PoemID> $element </PoemID>
            <PoemName> $poem </PoemName>
            <email> $email </email>
        </Poem>
EOF
        done
        echo "</Poems>"
 
    fi

fi


if [ $REQUEST_METHOD = "DELETE" ];then
    
    if [ -z $sessionID ];then
        echo "<Response><message>You are not logged in!!</message></Response>"


    else
        if [[ $REQUEST_URI =~ ^/(poem)+/[^/]*[0-9]$ ]];then
            poemID=`echo $REQUEST_URI | cut -d '/' -f 3`  
            owner=$(echo -n "select email from poem where poemID=\"$poemID\";" |  sqlite3 /usr/local/apache2/DB/userDB.db)
            email=$(echo -n "select email from Session where sessionID=\"$sessionID\"" |  sqlite3 /usr/local/apache2/DB/userDB.db )
            #echo $owner
            #echo $email
            if [ $owner = $email ];then
                echo "delete from Poem where poemID=\"$poemID\"" | sqlite3 /usr/local/apache2/DB/userDB.db
                echo "<Response><message>Poem deleted</message></Response>"
            else
                echo "<Response><message>You cannot delete this poem</message></Response>"

            fi
        
        fi

        if [ $REQUEST_URI = '/deleteall' ];then
            email=$(echo -n "select email from Session where sessionID=\"$sessionID\"" |  sqlite3 /usr/local/apache2/DB/userDB.db )
            #echo $owner
            #echo $email
            echo "delete from Poem where email=\"$email\"" | sqlite3 /usr/local/apache2/DB/userDB.db
            echo "<Response><message>All of your poems are deleted</message></Response>"
        fi
        
    fi
    
    

fi


if [ $REQUEST_METHOD = "PUT" ];then

    if [ -z $sessionID ];then
        echo "<Response><message>You are not logged in!!</message></Response>"

    else
            if [[ $REQUEST_URI =~ ^/(poem)+/[^/]*[0-9]$ ]];then
                poemID=`echo $REQUEST_URI | cut -d '/' -f 3`  
                owner=$(echo -n "select email from poem where poemID=\"$poemID\";" |  sqlite3 /usr/local/apache2/DB/userDB.db)
                email=$(echo -n "select email from Session where sessionID=\"$sessionID\"" |  sqlite3 /usr/local/apache2/DB/userDB.db )
                #echo $owner
                #echo $email
                if [ $owner = $email ];then
                    poem=`echo $BODY_RES | awk -F '<title>'  '{print $2}' | awk -F '</title>' '{print $1}'`
                    echo "update Poem set poem=\"$poem\" where poemID=\"$poemID\"" | sqlite3 /usr/local/apache2/DB/userDB.db
                    echo "<Response><message>Poem updated</message></Response>"
                else
                    echo "<Response><message>You cannot edit this poem</message></Response>"

            fi
        
    fi  


    fi
    

fi