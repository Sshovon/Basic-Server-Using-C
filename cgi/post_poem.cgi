#!/bin/sh

echo "Content-type: text/html; charset=utf-8"
echo ""

read -n $CONTENT_LENGTH POST_DATA <&0
poem=`echo "$POST_DATA" | awk '{split($0,array,"&")} END{print array[1]}' | awk '{split($0,array,"=")} END{print array[2]}'`
uid=`echo "$HTTP_COOKIE" | awk '{split($0,array,";")} END{print array[2]}' | awk '{split($0,array,"=")} END{print array[2]}'`
poem=$(echo "${poem//+/" "}")


echo -n "INSERT INTO Poem (poem, uid) VALUES (\"$poem\",\"$uid\" );" | sqlite3 /usr/local/apache2/DB/userDB.db

cat <<EOT
<!DOCTYPE html>
<html>
<head>
<title>Add poem</title>
</head>
<body>
<h3>Successfully added a new poem</h3>
</body>
</html>
EOT