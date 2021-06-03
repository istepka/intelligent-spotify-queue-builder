import os


def prep_env(client_id, client_secret):
    '''Set environmental variables.'''
    os.environ['SPOTIPY_CLIENT_ID'] = client_id
    os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
    print('Environmental variables set')



def prep_env_from_file(filename):
    '''Set environmental variables with credentials from local txt file. \n
    File should consist of 2 lines: \n
        client_id  \n
        client_secret'''
        
    with open(filename, 'r') as f:
        client_id = f.readline()
        client_secret = f.readline()
    
    os.environ['SPOTIPY_CLIENT_ID'] = client_id
    os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
    print('Environmental variables set')
