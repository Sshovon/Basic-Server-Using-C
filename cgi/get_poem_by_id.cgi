#!/bin/bash


echo "Content-type: application/xml; charset=utf-8"

echo ""
cat <<EOF
<Poems>
EOF

poemID=`echo "$QUERY_STRING" | awk '{split($0,array,"&")} END{print array[1]}' | awk '{split($0,array,"=")} END{print array[2]}'`


uid=$(echo -n "select uid from poem where poemID=\"$poemID\";" |  sqlite3 /usr/local/apache2/DB/userDB.db)
poem=$(echo -n "select poem from poem where poemID=\"$poemID\";" |  sqlite3 /usr/local/apache2/DB/userDB.db)
cat <<EOF
  <Poem>
    <PoemID> $poemID </PoemID>
    <PoemName> $poem </PoemName>
    <uid> $uid </uid>
  </Poem>
EOF



cat <<EOF
</Poems>
EOF