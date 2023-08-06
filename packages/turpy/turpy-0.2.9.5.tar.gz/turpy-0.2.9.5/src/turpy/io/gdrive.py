#taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
# https: // github.com/thoppe/streamlit-skyAR/blob/master/GD_download.py


import os
import requests
from pathlib import Path
from turpy.logger import log


def download_file(
    data_url: str,
    destination_filepath:str):
    """ Downloads a shared file given the google drive shared URL to 
    the destination filepath. 

    Args:
        data_url (str): example of expected URL `r"https://drive.google.com/file/d/<google_file_id>/view?`
        destination_filepath (str): [description]

    returns (status, local_downloaded_filepath)
    """
    dirpath = os.path.dirname(destination_filepath)
    assert os.path.isdir(dirpath)

    file_id = data_url.split('/')[-2]
    
    ## We require that the destination directory must exist.
    # save_dest = Path(dirpath)
    # save_dest.mkdir(exist_ok=True)

    f_checkpoint = Path(destination_filepath)

    if not f_checkpoint.exists():
        status = download_file_from_google_drive(
            id=file_id, 
            destination=destination_filepath
            )
    else:
        log.error(
            'Please ensure the `destination_filepath: {destination_filepath}` exist.')

    return status, f_checkpoint
    



def download_file_from_google_drive(id:str, destination:str):
    """Download a shared file from google drive and save it on destination.

    When downloading large files from Google Drive, a single GET request is not sufficient.
    A second one is needed, and this one has an extra URL parameter called confirm, 
    whose value should equal the value of a certain cookie.

    Args:
        id ([type]): [description]
        destination ([type]): [description]
    """
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    status = save_response_content(response, destination)

    return status


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    status = False
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                status = True

    return status

