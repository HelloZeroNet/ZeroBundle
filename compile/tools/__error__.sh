#!/bin/sh
#
# This is the default apptemplate error script
#
if ( test -n "$2" ) ; then
	echo "$1 Error"
	echo "An unexpected error has occurred during execution of the main script"
	echo ""
	echo "$2: $3"
	echo ""
	echo "See the Console for a detailed traceback."
else
	echo "$1 Error"
	echo ""
	echo "ERRORURL: https://github.com/HelloZeroNet/ZeroNet/issues/new Please report it"
fi
