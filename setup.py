import os


def prep_env(client_id, client_secret):
    '''Set environmental variables.'''
    os.environ['SPOTIPY_CLIENT_ID'] = client_id
    os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
    print('Environmental variables set')



def prep_env_from_file(filename='credentials.txt'):
    '''Set environmental variables with credentials from local txt file. \n
    File should consist of 2 lines: \n
        user_unique_spotify_name (not important within this function)\n
        client_id  \n
        client_secret'''
        
    with open(filename, 'r') as f:
        _ = f.readline()
        client_id = f.readline()
        client_secret = f.readline()
    
    os.environ['SPOTIPY_CLIENT_ID'] = client_id.strip("\n")
    os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret.strip("\n")
    print('Environmental variables set')


def get_spotify_username(filename='credentials.txt'):
    '''Get spotify unique username (id) from local txt file.\n
    First line of the file should contain this username.'''
    with open(filename, 'r') as f:
        name = f.readline().rstrip("\n")
    print('Username', name)
    return name

