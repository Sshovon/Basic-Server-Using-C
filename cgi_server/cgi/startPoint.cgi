#!/bin/bash
echo "Content-type: text/html"
echo ""


cat <<EOT
<!DOCTYPE html>
<html>
<head>
        <title>Welcome to our application</title>
</head>
<body>
        <p>Hello! Please enter your userID and password and press the submit button to register</p>
        <form action="reg.cgi" method="post">
                <label>UserID</label>
                <input type="text" name="uid">
                <br>
                <label>Password</label>
                <input type="password" name="password">
                <br>
                <button type="submit">Register</button>
        </form>
        <br><br><br>
        <p>Hello! Please enter your userID and password and press the submit button to login</p>
        <form action="login.cgi" method="post">
                <label>UserID</label>
                <input type="text" name="uid">
                <br>
                <label>Password</label>
                <input type="password" name="password">
                <br>
                <button type="submit">Login</button>
        </form>
</body>
</html>
EOT

