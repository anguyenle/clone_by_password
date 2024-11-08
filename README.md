# clone_by_password
This is an awful tool for wrapping git ssh commands, and is intended to let you clone from private repositories without needing to log in. Nobody should use this because it eschews security for convenience, which is always a bad thing. We personally never use it because our security practices are top notch.

After setting up our repo, it is designed to work in one line with no persistent changes to any system this is run from (except for needing to install pycryptodome, but ¯\\\_(ツ)_/¯). This script requires [pycryptodome](https://pycryptodome.readthedocs.io/en/latest/), and works by seeding the RSA key generation process with deterministic noise which pretty much acts like a password.

## Example usage:

### Setup
The setup tool reports a public key straight to your terminal. You should copy and paste its output into the deployment keys in the repository you want to be able to access.
```
python wrap_git.py setup "password"
```
One annoying thing that can happen is that your terminal may add line-breaks that mess with copy/pasting. In this case, you can write the public key to a file and copy from there.
```
python wrap_git.py setup "password" --filename "access_key.pub"
```
### Cloning
```
python wrap_git.py "password" "git clone git@github.com:anguyenle/clone_by_password.git"
```

## Testing
We've successfully gotten this script to run on our Linux Machine, on cloud servers rented from Salad, and on Google Colab. A bug that shows up intermittendtly is that a system reports that it adds Github to the known_hosts file (even though it cannot); we think we've ironed this one out but who knows.
