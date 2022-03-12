#!/bin/sh
#header
	#echo header
	cookie = $( echo $HTTP_COOKIE)
	if [ "$cookie" != "" ]; then
		echo "Set-cookie:diktsejsonsid=$cookie"
	fi
	# if login
	if [ "$email" != "" || "$passord" != "" ]; then
		curlresult = $(echo curl localhost:$port -d "<bruker><epostadresse>$email</epostadresse><passord>$password</passord></bruker>")
		cookie = $(echo $curlresult | cut -c 35-5 | cut -d "<" f 1)#cut from return "<diktdatabase><Sesjon><sesjonsID>$sessionID</sesjonsID><epostadresse>$emailadress</epostadresse></Sesjon></diktdatabase>
		if [ "$cookie" != "" ]; then
			echo "Set-cookie:diktsejsonsid=$cookie" #set cookie command $cookie
		fi
		if [ "$cookie" = "" ]; then
			echo "Login failed"
		fi
	fi
	# if logout   SJEKK MED SINDRE
	logout = $( echo $BODY | cut -d "=" f 2 | awk '{ print substr( $0, 1, lenght($0)-13)}')
	if [ "$logout" = "logout" ]; then
		curl -X DELETE localhost:8080/diktdatabase/sesjon/sesjonsID/$cookie
	fi
	
#/header
echo ""
#body
# check request method
	
 if [ "$REQUEST_METHOD" != "POST" ]; then
	echo "request method not valid"
 fi
 
 elif [ "REQUEST_METHOD" = "POST" ]; then

	# logout=logout&epostadresse=test123&passord=test123&spørring=test123&diktID=test123&dikt=test123
	# variabels
	
	logout = $( echo $BODY | cut -d "=" f 2 | awk '{ print substr( $0, 1, lenght($0)-13)}')
	
	email = $( echo $BODY | cut -d "=" f 3 | awk '{ print substr( $0, 1, lenght($0)-8)}')
	password = $(echo $BODY | cut -d "=" f 4 | awk '{ print substr( $0, 1, lenght($0)-9)}')
	button = $(echo $BODY | cut -d "=" f 5 | awk '{ print substr( $0, 1, lenght($0)-7)}')
	diktID = $(echo $BODY | cut -d "=" f 6 | awk '{ print substr( $0, 1, lenght($0)-5)}')
	dikt = $(echo $BODY | cut -d "=" f 6)
	port = 8080
	
	login = $( curl --cookie "diktsejsonsid=$cookie" localhost:$port ) # får "<diktdatabase><Sesjon><sesjonsID>$sessionID</sesjonsID><epostadresse>$emailadress</epostadresse></Sesjon></diktdatabase>
	


	# legge inn URL til gruppe siden
	# Form
	echo "<!DOCTYPE html>"
	echo "<html>"
	echo "<body>"

	echo "<h1>Innloging til Diktdatabase</h1>"
	# check if logged in or not
		echo "<form method="post">"
	if [ "$login" = true ]; then
		# print log out
		
			echo "<input type="hidden" id="logout" name="logout" value= "logout">"
			echo "<button name="logout" type="submit" value="logout">"
			
			echo "<input type="hidden" id="epostadresse" name="epostadresse"><br><br>"
			echo "<input type="hidden" id="passord" name="passord" minlength="8"><br><br>"
	fi 
	if [ "$login" != true ]; then
		# if not print login
		
			echo "<input type="hidden" id="logout" name="logout" value= "logout">"

			echo "<label for="email">E-post adresse:</label><br>"
			echo "<input type="email" id="epostadresse" name="epostadresse"><br><br>"
			echo "<label for="pwd">Passord:</label><br>"
			echo "<input type="password" id="passord" name="passord" minlength="8"><br><br>"
			echo "<input type="submit" value="Logge inn:">"
	fi
		echo "</form>"
	echo "<h2>Spørringer</h2>"

	echo "<p>Velg spørring:</p>"
	echo "<form method = "post">"
	  	echo "<input type="radio" id="spørring1" name="spørring" value="spørring1">"
		echo "<label for="spørring1">hente ut ett bestemt dikt (gitt diktID),</label><br>"
		echo "<input type="radio" id="spørring2" name="spørring" value="spørring2">"
		echo "<label for="spørring2">hente alle dikt</label><br>"
		# check if logged in or not
		if [ "$login" = true]; then
			echo "<input type="radio" id="spørring3" name="spørring" value="spørring3">"
			echo "<label for="spørring3">legge til nytt dikt:</label><br>"
			echo "<input type="radio" id="spørring4" name="spørring" value="spørring4">"
			echo "<label for="spørring4">endre egne dikt,</label><br>"
			echo "<input type="radio" id="spørring5" name="spørring" value="spørring5">"
			echo "<label for="spørring5">slette eget dikt (gitt diktID)</label><br>"
			echo "<input type="radio" id="spørring6" name="spørring" value="spørring6">"
			echo "<label for="spørring6">slette alle egne dikt</label><br><br>"
			echo "<label for="diktID">vennligst legge inn diktID:</label>"
			echo "<input type="text" id="diktID" name="diktID"><br><br>"
			echo "<textarea name="Dikt" style="width:200px; height:100px;">"
			echo "Legg til ditt dikt her....</textarea><br>"
		fi
		if [ "$login" != true ]; then
			echo "<input type="hidden" id="diktID" name="diktID"><br><br>"
		fi
		echo "<input type="submit" value="Submit">"
	
	
	echo "</form>"
		# Action based on radiobutton value

	if [ "$button" = "spørring1"]; then
		# hent ett 
		curlreturn = $( 'curl --cookie "diktsejsonsid=$cookie" localhost:$port/diktdatabase/dikt/$diktID')
	fi

	elif [ "$button" = "spørring2"]; then
		# hent alle
		curlreturn = $( 'curl --cookie "diktsejsonsid=$cookie" localhost:$port/diktdatabase/dikt/')
	fi
	elif [ "$button" = "spørring3"]; then
		# sett inn	curl -d "<dikt><id>1</id><tittel>Skrønebok</tittel></bok>"  localhost:8080/bokbase/bok/
		curlreturn = $( 'curl -d "<Dikt><dikt>$dikt</dikt></Dikt>" --cookie "diktsejsonsid=$cookie" localhost:$port/diktdatabase/dikt/')
	fi
	elif [ "$button" = "spørring4"]; then
		# endre		curl -X PUT -d "<bok><tittel>Skrønebok</tittel></bok>"  localhost:8080/bokbase/bok/1
		curlreturn = $( 'curl -X PUT -d "<Dikt><dikt><dikt>$dikt</dikt></bok>" --cookie "diktsejsonsid=$cookie" localhost:$port/diktdatabase/dikt/$diktID')
	fi
	elif [ "$button" = "spørring5"]; then
		# slett		curl -X DELETE localhost:8080/bokbase/bok/1
		curlreturn = $( 'curl -X DELETE --cookie "diktsejsonsid=$cookie" localhost:$port/diktdatabase/dikt/$diktID')

	fi
	elif [ "$button" = "spørring6"]; then
		# slett		curl -X DELETE localhost:8080/bokbase/bok/
		curlreturn = $(echo 'curl -X DELETE --cookie "diktsejsonsid=$cookie" localhost:$port/diktdatabase/dikt/')
	fi

	# print XML return 
	# for each line 

	while IFS= read -r line; do
		echo "$line"
	done <<< "$curlreturn"

	
	echo "</body>"
	echo "</html>"

fi

# login retur vil se slik ut 		echo "<diktdatabase><sesjonsID>$sessionID</sesjonsID><epostadresse>$emailadress</epostadresse></diktdatabase>"




