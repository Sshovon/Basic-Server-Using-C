#!/bin/sh
echo "Content-type: text/html"
echo ""




echo $QUERY_STRING


cat <<EOT
<!DOCTYPE html>
<html>
<head>
        <title>Welcome to our application</title>
</head>
<body>
        <p>$HTTP_COOKIE</p>
</body>
</html>