#!/bin/bash
#cat <<EOF                      
#Content-type: application/xml; charset=utf-8
#EOF
#echo

cat <<EOF                      
<?xml version="1.0"?>          
<poem>                         
EOF

#get user email from session id. if the user is loggined, the email will be not empty.
export USER_EMAIL=$(echo -n -e "SELECT email FROM Session WHERE sessionId = $SESSION_ID;" | sqlite3 /var/www/poem.db -line | \
                              sed 's/[[:blank:]]*\(.*\) = \(.*$\)/\2/')

#if user loggined add the poem with the email
if [ ! -z $USER_EMAIL ]; then

  export POEM=$(xmlstarlet  sel -T -t -m /Poem  -v "concat('\"',poem,'\"')" -n $XML_FILE_NAME);

  if [[ $XML_FILE_NAME =~ \.xml$ ]]; then
    rm $XML_FILE_NAME
  fi

  echo $POEM >> pm.txt
  echo -e -n "INSERT INTO \"Poem\"(\"poem\", \"email\") VALUES ($POEM, \"$USER_EMAIL\"); SELECT last_insert_rowid() ;"  | \
    sqlite3 /var/www/poem.db -line | \
    sed 's/[[:blank:]]*\(.*\) = \(.*$\)/\t<poemfield>\2<\/poemfield>/'
else
  Not loggined
fi
# echo -n 'select * from bok' | \
# mysql -h debbie -u db -pada --xml --default-character-set=utf8 bokbase
  
cat <<EOF
</poem>
EOF

