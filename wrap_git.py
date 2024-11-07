import argparse
import os
import random
from Crypto.PublicKey import RSA

# Requirements, pycryptodome.

def setup_git_wrapper(seed_string,
                      filename = None):
    '''
    Setup Git
    '''
    random.seed(a=seed_string, version=2)
    # Generate the RSA key pair
    key = RSA.generate(2048, randfunc=random.randbytes)

    # Grab the public key in OpenSSH format
    public_key = key.publickey().export_key(format='OpenSSH')

    if filename is None:
        message = (
        "Please copy and paste the following public key into your "
        "repository's deploy keys. This can be found in Settings > "
        "Deploy Keys. Alternatively, if the key is too long to "
        "comfortably copy, please specify a directory; you just "
        "need to copy this and ensure there's no linebreaks "
        "introduced by your shell."
        )

        
        print(message)
        print(public_key.decode())
    else:
        with open(filename, "w+") as f:
            f.write(public_key.decode())   
 

def wrap_git_ssh(seed_string,
                 git_command,
                 private_key_filename = 'access_key'):
    '''
    The only tested use case is to git-clone from a private repo with 
    something resembling a password.

    Arguments:

    seed_string : This is pretty much a password
    git_command : This command is what you want to do. If you want
        to git-clone, you should pretty much copy-paste from Github.
    
    private_key_filename : The name of the private key. This file will
        be stored in the current directory, and deleted after runtime.
        The default is 'access_key'.

    '''

    current_working_directory = os.getcwd() + "/"

    random.seed(a=seed_string, version=2)
    # Generate the RSA key pair
    key = RSA.generate(2048, randfunc=random.randbytes)

    # Export the private key in PEM format
    private_key = key.export_key(format='PEM')
    private_string = private_key.decode()

    temp_file_dir = current_working_directory + private_key_filename

    # Write the key
    with open(temp_file_dir, "w+") as f:
        f.write(private_string)

    # Temporarily add a enviroment variable to whatever shell we're in.

    os.environ['GIT_SSH_COMMAND'] = \
        'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o "LogLevel ERROR" -i ' + temp_file_dir
e
    # Restrict the key permissions, or else SSH will complain.
    os.system("chmod go-rwx " + temp_file_dir)

    # Now we can clone stuff with no additional nonsense.
    error_flag = os.system(git_command)
    if error_flag:
        print("Git command failed with code " + str(error_flag))
    
    del os.environ['GIT_SSH_COMMAND']
    os.remove(temp_file_dir)
                   
def main():
    parser = argparse.ArgumentParser(description="Git SSH Wrapper Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Parser for setup_git_wrapper
    parser_setup = subparsers.add_parser("setup", help="Setup Git with a new SSH key")
    parser_setup.add_argument("seed_string", help="Seed string for generating the SSH key")
    parser_setup.add_argument("--filename", help="Optional filename to save the public key")

    # Parser for wrap_git_ssh
    parser_wrap = subparsers.add_parser("wrap", help="Wrap a Git command with SSH key")
    parser_wrap.add_argument("seed_string", help="Seed string for generating the SSH key")
    parser_wrap.add_argument("git_command", help="Git command to run (e.g., 'git clone <repo-url>')")
    parser_wrap.add_argument("--private_key_filename", default="access_key", help="Name of the private key file (default: access_key)")

    args = parser.parse_args()

    if args.command == "setup":
        setup_git_wrapper(args.seed_string, args.filename)
    elif args.command == "wrap":
        wrap_git_ssh(args.seed_string, args.git_command, args.private_key_filename)

if __name__ == "__main__":
    main()

