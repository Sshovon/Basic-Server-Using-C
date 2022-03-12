#!/bin/sh
echo "Content-type: text/xml; charset=utf-8"
echo ""


cat <<EOF
<?xml version="1.0"?>

<Poems>                      
EOF

  echo -n 'select * from user;'  | sqlite3 /usr/local/apache2/DB/userDB.db -line 
    
cat <<EOF
</Poems>
EOF
