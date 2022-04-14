#!/bin/bash
#header

echo "Content-type: text/html"
echo ""

#header

cat <<EOT
<!DOCTYPE html>
<html>
<head>
        <title>Welcome to our application</title>
</head>
<body>
        <p>Hello! Please enter your userID and password and press the register button to register</p>
        <form action="reg.cgi" method="post">
                <label>UserID</label>
                <input type="text" name="uid">
                <br><br>
                <label>Password</label>
                <input type="password" name="password">
                <br><br>
                <label>First Name</label>
                <input type="text" name="fname">
                <br><br>
                <label>Last Name</label>
                <input type="text" name="lname">
                <br><br>
                <button type="submit">Register</button>
        </form>
        <br><br><br>
        <p>Hello! Please enter your userID and password and press the login button to login</p>
        <form action="login.cgi" method="post">
                <label>UserID</label>
                <input type="text" name="uid">
                <br><br>
                <label>Password</label>
                <input type="password" name="password">
                <br><br>
                <button type="submit">Login</button>
        </form>
</body>
</html>
EOT

