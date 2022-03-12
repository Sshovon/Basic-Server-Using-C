#!/bin/bash

echo
echo Creating database.
echo


sqlite3 /usr/local/apache2/DB/userDB.db <<EOF

DROP TABLE IF EXISTS User;

CREATE TABLE User (
    uid     STRING PRIMARY KEY
                     UNIQUE
                     NOT NULL,
    password  STRING
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

INSERT INTO User (uid, password) VALUES ("test@uid.com", "c5ca90f6c70d2da6090ce55f9c1c920984196279e25587147184f88412c6e7fa");

INSERT INTO Poem (poemID, poem, uid) VALUES (1, "Hello there", "test@uid.com");
INSERT INTO Poem (poemID, poem, uid) VALUES (2, "General kenobi", "another@uid.com");

EOF

echo Database has been created.
echo
echo Setting permissions and ownership.
#chown root /usr/local/apache2/DB/userDB.db
chmod 777 /usr/local/apache2/DB/userDB.db

echo
echo Ownership and permissions set. Program will now exit.
