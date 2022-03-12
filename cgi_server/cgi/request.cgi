#!/bin/sh
echo "Content-type:text/xml;charset=utf-8"
echo ""
echo REQUEST_METHOD -req : $REQUEST_METHOD
echo REQUEST_URI : -req $REQUEST_URI
echo

if [ "$REQUEST_METHOD" = "GET" ]; then
	echo "GET method called"
	# if [ -z "${REQUEST_URI##*"/poems/"*}" ]; then
	# 	#/var/www/get_all_poems.cgi
	# 	echo "poems method called"
	# fi
	if [ ${REQUEST_URI}="/poems/" ];then

		echo "give hime poems"

	fi


	if [ -z "${REQUEST_URI##*"/poem/"*}" ]; then
		#/poem/[session id]/[poem id]/
		export POEM_ID=$(cut -d '/' -f 3 <<< $REQUEST_URI)
		/var/www/get_poem.cgi
		echo "get poem called"
	fi

	if [ -z "${REQUEST_URI##*"/logout/"*}" ]; then
		export SESSION_ID=$(cut -d '/' -f 3 <<< $REQUEST_URI)
		/var/www/log_out.cgi
		echo "logout called"
	fi
fi


if [ "$REQUEST_METHOD" = "POST" ]; then
	if [ -z "${REQUEST_URI##*"/poem/"*}" ]; then
		echo "xml : $XML_FILE_NAME"
		export SESSION_ID=$(cut -d '/' -f 3 <<< $REQUEST_URI)
		/var/www/post_poem.cgi
	fi

	if [ "$REQUEST_URI" = "/login" ]; then
		/var/www/login.cgi
	fi

fi


if [ "$REQUEST_METHOD" = "PUT" ]; then
	echo
	  if [ -z "${REQUEST_URI##*"/update_poem/"*}" ]; then
  		export POEM_ID_UPDATE=$(cut -d '/' -f 4 <<< $REQUEST_URI)
			export SESSION_ID=$(cut -d '/' -f 3 <<< $REQUEST_URI)
			/var/www/change_own_poem.cgi
		fi
fi


if [ "$REQUEST_METHOD" = "DELETE" ]; then
	if [ -z "${REQUEST_URI##*"/delete_poem/"*}" ]; then
		export POEM_ID_DELETE=$(cut -d '/' -f 4 <<< $REQUEST_URI)
		export SESSION_ID=$(cut -d '/' -f 3 <<< $REQUEST_URI)
		/var/www/delete_poem.cgi
	fi

  if [ -z "${REQUEST_URI##*"/delete_all_poems/"*}" ]; then
		export SESSION_ID=$(cut -d '/' -f 3 <<< $REQUEST_URI)
	  /var/www/delete_all_user_poems.cgi
	fi
fi

