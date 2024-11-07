# clone_by_password
This is an awful tool for wrapping git ssh commands, and is intended to let you clone from private repositories without needing to log in. After setup, it is designed to work in one line. This script requires [pycryptodome](https://pycryptodome.readthedocs.io/en/latest/) works by seeding the RSA key generation process with seedable noise. Further, this script is designed to not change anything systemwide; after it runs, it should delete every temporary file it needed to create to work with git ssh commands.

## Example usage:

### Setup
The setup tool reports a public key straight to your terminal. You should copy and paste its output into the deployment keys in the repository you want to be able to access.
```
python clone_by_password.py setup "password"
```
One annoying thing that can happen is that your terminal may add line-breaks that mess with copy/pasting. In this case, you can write the public key to a file and copy from there.
```
python clone_by_password.py setup "password" --filename "access_key.pub"
```
### Cloning
```
python clone_by_password.py "password" "git clone git@github.com:anguyenle/clone_by_password.git"
```

