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
    git_command : This command should be copy-pasted from Github.
    
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
