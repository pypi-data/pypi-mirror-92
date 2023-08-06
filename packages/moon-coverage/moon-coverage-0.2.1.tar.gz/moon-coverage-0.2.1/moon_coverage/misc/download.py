"""Generic web download method."""

from pathlib import Path
from urllib.request import urlretrieve


def wget(url, fout, skip=False, force=False, verbose=True):
    """Web download.

    Parameters
    ----------
    url: str
        URL to download
    fout: str or Path
        Output file.
    skip: bool, optional
        Skip download if the output file already exists (default: `False`).
        Has the priority over :py:attr:`force`.
    force: bool, optional
        Force download even if the file exists (default: `False`).
    verbose: bool, optional
        Verbose download.

    Returns
    -------
    pathlib.Path
        Downloaded file path.

    Raises
    ------
    FileExistsError
        If the file already exists.

    Note
    ----
    The missing sub-directories will be created.

    """
    fname = Path(fout)

    if fname.exists():
        if skip:
            return fname
        if not force:
            raise FileExistsError(fname)

    if not fname.exists() or force:
        # Create sub directories (if missing)
        fname.parent.mkdir(parents=True, exist_ok=True)

        # Download the content and save it in `fname`
        if verbose:
            print(f'> Downloading: {url}', end='')

        urlretrieve(url, fname)

        if verbose:
            print(' -- Success')

    return fname
