import gdown



def get_file_Drive(url : str, output :str):
    """
    Download a file from Google Drive using gdown.

    Args: 
        url (str): The Google Drive URL pointing to the file to download. 
        output (str): The destination path where the downloaded file will be saved.
        
    Returns:
        None

    """
    gdown.download(url, output, quiet=False)