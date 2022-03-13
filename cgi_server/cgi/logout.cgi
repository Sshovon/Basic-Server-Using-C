#!/bin/sh
echo "Content-type: text/html"


sessionID=`echo "$HTTP_COOKIE" | awk '{split($0,array,";")} END{print array[1]}' | awk '{split($0,array,"=")} END{print array[2]}'`
del=`echo -e -n "DELETE FROM Session WHERE sessionID = \"$sessionID\" ;" |  sqlite3 /usr/local/apache2/DB/userDB.db`
echo "Set-cookie:sessionID="
echo "Set-cookie:uid="
echo "Set-cookie:status=0"

echo ""



cat <<EOT
<!DOCTYPE html>
<html>
<head>
<title>Logout</title>
</head>
<body>
<h3>Successfully logged out</h3>
</body>
</html>