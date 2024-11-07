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
        message = "Please copy and paste the following public key into your repository's deploy keys. This can be found in Settings > Deploy Keys. Alternatively, if the key is too long to comfortably copy, please specify a directory."
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

    current_working_directory = os.getcwd()

    random.seed(a=seed_string, version=2)
    # Generate the RSA key pair
    key = RSA.generate(2048, randfunc=random.randbytes)

    # Export the private key in PEM format
    private_key = key.export_key(format='PEM')
    private_string = private_key.decode()

    # Export the public key in OpenSSH format
    #public_key = key.publickey().export_key(format='OpenSSH')

    temp_file_dir = current_working_directory + private_key_filename

    # Write the key
    with open(temp_file_dir, "w+") as f:
        f.write(private_string)

    # Temporarily add a enviroment variable to whatever shell we're
    # in. This one is pretty benign.

    os.environ['GIT_SSH_COMMAND'] = \
        'ssh -o StrictHostKeyChecking=no -i ' + temp_file_dir

    # Restrict the key permissions, or else SSH will complain.
    os.system("chmod go-rwx " + temp_file_dir)

    # Now we can clone stuff with no additional nonsense.
    error_flag = os.system(git_command)
    if error_flag:
        print("Git command failed with code " + str(error_flag))
    
    del os.environ['GIT_SSH_COMMAND']
    os.remove(temp_file_dir)

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="A convenient way to access git private repos.")
    
    # The function to call (either 'setup_git_wrapper' or 'wrap_git_ssh')
    parser.add_argument("func", nargs="?", default="wrap_git", 
                        choices=["setup", "wrap_git"], 
                        help="Which function to run: 'setup_git_wrapper' or 'wrap_git_ssh'")

    # Common argument: seed_string
    parser.add_argument("seed_string", type=str, help="The seed string, which acts as a password)")

    # Additional arguments based on the selected function
    parser.add_argument("git_command", type=str, nargs="?", 
                        help="Git command to run (used only with wrap_git_ssh)")

    parser.add_argument("filename", type=str, nargs="?", default=None, 
                        help="Filename to save keys")

    # Parse arguments
    args = parser.parse_args()

    # Run the appropriate function
    if args.func == "setup":
        setup_git_wrapper(args.seed_string, args.filename)
    elif args.func == "wrap_git_ssh":
        if not args.git_command:
            print("Error: You must provide a git command when using 'wrap_git_ssh'.")
        else:
            wrap_git_ssh(args.seed_string, args.git_command)

if __name__ == "__main__":
    main()

