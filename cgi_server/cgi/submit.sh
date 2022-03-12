#!/bin/sh
echo "Content-type: text/html"
echo ""


echo $QUERY_STRING
uid=`echo "$QUERY_STRING" | awk '{split($0,array,"&")} END{print array[1]}' | awk '{split($0,array,"=")} END{print array[2]}'`
password=`echo "$QUERY_STRING" | awk '{split($0,array,"&")} END{print array[2]}' | awk '{split($0,array,"=")} END{print array[2]}'`

echo $uid
echo $password

cat <<EOT
<!DOCTYPE html>
<html>
<head>
        <title>Welcome to our application</title>
</head>
<body>
        <h1>Welcome $uid </h1>
        <h2> Your e-mail address is $password <h2>
</body>
</html>