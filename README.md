# clone_by_password
This is an awful tool for wrapping git ssh commands. After setup, it is designed to work in one line.

## Example usage:

### Setup

python clone_by_password.py setup "password"
python clone_by_password.py setup "password" --filename "access_key.pub"

### Cloning
python clone_by_password.py "password" "git clone git@github.com:anguyenle/clone_by_password.git"

This script requires [pycryptodome](https://pycryptodome.readthedocs.io/en/latest/) works by seeding the RSA key generation process with deterministic noise.
