#!/bin/bash


echo "Content-type: application/xml; charset=utf-8"
echo ""


cat <<EOF
<Poems>
EOF


#extracting email from cookie
email=`echo "$HTTP_COOKIE" | awk '{split($0,array,";")} END{print array[2]}' | awk '{split($0,array,"=")} END{print array[2]}'`

#now extracting how many poem you have in database 
poems=$(echo "select poemID from poem where email=\"$email\";" | sqlite3 /usr/local/apache2/DB/userDB.db)
#converting db query result into string
poems=$(echo $poems)
# internal field seperator that means we are going to seperate string based on space " "
IFS=" "

# <<< means reading from a string and storing each word / part into a array
read -ra arr <<< "$poems"

# looping / traversing into the array
#element is poemID
for element in "${arr[@]}"
do 
  #searching in database for information of the poem using poemID
  #and you are the owner so you dont have to search email in database
  poem=$(echo -n "select poem from poem where poemID=\"$element\";" |  sqlite3 /usr/local/apache2/DB/userDB.db)
  cat <<EOF
  <Poem>
    <PoemID> $element </PoemID>
    <PoemName> $poem </PoemName>
    <email> $email </email>
  </Poem>
EOF
done


cat <<EOF
</Poems>
EOF