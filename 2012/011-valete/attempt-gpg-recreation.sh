#!/usr/bin/env python3

./monkeysphere/src/pem2openpgp "it worked" < recreated.pem | gpg2 --import --homedir temp_gpg/
