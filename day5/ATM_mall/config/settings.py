user_info = {
    "my_shop": {
        }
    , "admin_bank": {
        "admin": {
            "birthday": "", "age": "", "mail": "", "contact": "", "level": "0", "en_name": "", "password": "ca09b0783e7dd733b45f5908ec79f040", "cn_name": ""
            }
        }
    , "account_info": {
        }
    , "my_bank": {
        }
    }


import hashlib
aaaa = hashlib.md5()
aaaa.update(str(0).encode('utf-8'))
ass = aaaa.hexdigest()
print(ass)
print(len(ass))