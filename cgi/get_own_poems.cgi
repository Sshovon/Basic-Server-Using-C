#!/bin/bash


echo "Content-type: application/xml; charset=utf-8"

echo ""
cat <<EOF
<Poems>
EOF

uid=`echo "$HTTP_COOKIE" | awk '{split($0,array,";")} END{print array[2]}' | awk '{split($0,array,"=")} END{print array[2]}'`

poems=$(echo "select poemID from poem where uid=\"$uid\";" | sqlite3 /usr/local/apache2/DB/userDB.db)
poems=$(echo $poems)
IFS=" "
read -ra arr <<< "$poems"

for element in "${arr[@]}"
do 
  poem=$(echo -n "select poem from poem where poemID=\"$element\";" |  sqlite3 /usr/local/apache2/DB/userDB.db)
  cat <<EOF
  <Poem>
    <PoemID> $element </PoemID>
    <PoemName> $poem </PoemName>
    <uid> $uid </uid>
  </Poem>
EOF
done


cat <<EOF
</Poems>
EOF