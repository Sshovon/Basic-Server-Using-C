#!/bin/sh

echo
echo Creating database named userDB.db
echo

sqlite3 /usr/local/apache2/DB/userDB.db <<EOF

DROP TABLE IF EXISTS User;

CREATE TABLE User (
    uid     STRING PRIMARY KEY
                     UNIQUE
                     NOT NULL,
    password  STRING,
    fname STRING,
    lname STRING
);

DROP TABLE IF EXISTS Poem;

CREATE TABLE Poem (
    poemID INTEGER PRIMARY KEY
                   AUTOINCREMENT,
    poem   STRING,
    uid          REFERENCES User (uid)
                   NOT NULL
);

DROP TABLE IF EXISTS Session;

CREATE TABLE Session (
    sessionID STRING  NOT NULL
                      PRIMARY KEY
                      UNIQUE,
    uid     STRING  REFERENCES User (uid)
                      NOT NULL
);

INSERT INTO Poem (poem, uid) VALUES ("sams story", "sam");
INSERT INTO Poem (poem, uid) VALUES ("beautiful", "shakespeare");
INSERT INTO Poem (poem, uid) VALUES ("Hello ", "nazrul");
INSERT INTO Poem (poem, uid) VALUES ("dui bigha jomi", "kazi");

EOF

echo Database has been created.
echo
echo Setting permissions and ownership.
#chown root /usr/local/apache2/DB/userDB.db
chmod 777 /usr/local/apache2/DB/userDB.db

echo
echo Ownership and permissions set. Program will now exit.
