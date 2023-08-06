# py-bsdauth

- Python interface to OpenBSD's BSD Auth
- Currently only implements auth_userokay(3) since this is most suitable for authenticating to OpenBSD from python

### Note
- Your application must have root privileges in order to use this module.

Usage:
```sh
>>> from bsdauth.bsdauth import UserOkay
>>> u='user1'
>>> pw='goodpassword'
>>> uo=UserOkay(u,pw)
>>> uo.login()
True
>>> pw='badpassword'
>>> uo = UserOkay(ur,pw)
>>> uo.login()
False
>>> ur='baduser'
>>> pw='goodpassword'
>>> uo = UserOkay(ur,pw)
>>> uo.login()
False
>>> exit()
```
