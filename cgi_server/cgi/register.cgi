#!/bin/bash
#cat <<EOF                      
#Content-type: application/xml; charset=utf-8
#EOF
#echo

cat <<EOF                      
<?xml version="1.0"?>          
<poem>                         
EOF


export XML_VALUES=$(xmlstarlet  sel -T -t -m /Poem  -v "concat('\"',poem,'\",\"', email, '\"')" -n $XML_FILE_NAME);

if [[ $XML_FILE_NAME =~ \.xml$ ]]; then
  rm sended*.xml
fi

echo $XML_VALUES >> pm.txt
echo -e -n "INSERT INTO \"Poem\"(\"poem\", \"email\") VALUES ($XML_VALUES); SELECT last_insert_rowid() ;"  | \
  /var/www/sqlite3 poem.db -line | \    
  sed 's/[[:blank:]]*\(.*\) = \(.*$\)/\t<poemfield navn="\1">\2<\/poemfield>/'
# echo -n 'select * from bok' | \
# mysql -h debbie -u db -pada --xml --default-character-set=utf8 bokbase
  
cat <<EOF
</poem>
EOF

