#!/bin/bash

echo "Content-type: application/xml; charset=utf-8"
echo ""


cat <<EOF
<Poems>
EOF


#searching poem from database based on poemID
poemID=`echo "$QUERY_STRING" | awk '{split($0,array,"&")} END{print array[1]}' | awk '{split($0,array,"=")} END{print array[2]}'`

#getting the email and poem using the poemID
email=$(echo -n "select email from poem where poemID=\"$poemID\";" |  sqlite3 /usr/local/apache2/DB/userDB.db)
poem=$(echo -n "select poem from poem where poemID=\"$poemID\";" |  sqlite3 /usr/local/apache2/DB/userDB.db)

#creating a xml
cat <<EOF
  <Poem>
    <PoemID> $poemID </PoemID>
    <PoemName> $poem </PoemName>
    <email> $email </email>
  </Poem>
EOF



cat <<EOF
</Poems>
EOF