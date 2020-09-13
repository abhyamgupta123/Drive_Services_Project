#!/bin/bash

echo "Installing all required Libraries..."
echo " "
echo "Python Libraries are :--
          -> google-api-python-client
          -> google-auth-httplib2
          -> google-auth-oauthlib
          -> oauth2client
          "

pip2 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip2 install --upgrade oauth2client
