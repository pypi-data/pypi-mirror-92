# PygAuth
A Python helper library for Google Authentication
# Installation
Install from pypi! https://pypi.org/project/pygauth/
# Usage
### Get Service Account Credentials
```
get_sa_creds(sa_file: Union[str, Path], scopes: List[str] = None)

sa_file: file to read SA creds from
scopes: list of scopes to auth with
```
##### Examples:
```python
pygauth.get_sa_creds("creds.json") # get sa creds with no scopes
pygauth.get_sa_creds("creds.json", scopes=["drive"]) # get sa creds using shorthand scope
pygauth.get_sa_creds("creds.json", scopes=["https://www.googleapis.com/auth/drive"]) # get sa creds using longhand scope
```
### Get User Account Credentials
##### From File:
```
get_user_creds_file(creds_file: Union[str, Path], scopes: List[str] = None, create_cache: bool = True, refresh_cache: bool = False, remote: bool = False)

creds_file: file to read oauth portal credentials from
scopes: list of scopes to auth with
create_cache: whether to use the .pygauth cache file
refresh_cache: overwrites whatever is cached with a new value automatically
remote: whether to use remote auth or local auth (use when on a headless server)
```
##### From Dict:
```
get_user_creds_dict(creds_dict: Dict[str, str], scopes: List[str] = None, create_cache: bool = True, refresh_cache: bool = False, remote: bool = False)

creds_dict: dictionary of oauth portal credentials
scopes: list of scopes to auth with
create_cache: whether to use the .pygauth cache file
refresh_cache: overwrites whatever is cached with a new value automatically
remote: whether to use remote auth or local auth (use when on a headless server)
```
##### Examples:
```python
>>> creds_dict = json.load(open("credentials.json"))
>>> creds = pygauth.get_user_creds_file("credentials.json", scopes=["drive"]) # authenticate using file
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth ...
>>> creds = pygauth.get_user_creds_dict(creds_dict, scopes=["iam"]) # authenticate using dict
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth ...
>>> creds = pygauth.get_user_creds_file("credentials.json", scopes=["drive"]) # authenticate using file
# doesn't ask for another login since this scope has already been authenticated
```

