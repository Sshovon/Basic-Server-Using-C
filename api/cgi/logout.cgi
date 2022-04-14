#!/bin/sh
echo "Content-type: text/html"

#extracting sessionID from cookie
sessionID=`echo "$HTTP_COOKIE" | awk '{split($0,array,";")} END{print array[1]}' | awk '{split($0,array,"=")} END{print array[2]}'`
#deleting session id from database
del=`echo -e -n "DELETE FROM Session WHERE sessionID = \"$sessionID\" ;" |  sqlite3 /usr/local/apache2/DB/userDB.db`
#cleaing sessionID from cookie
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
<form >
    <button type="submit" formaction="startPoint.cgi">OK</button>
</form>
</body>
</html>
EOT