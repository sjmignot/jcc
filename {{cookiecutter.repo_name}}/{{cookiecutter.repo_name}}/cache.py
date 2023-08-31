from datetime import datetime
import os
from shutil import make_archive, unpack_archive
from utils import upload_file_to_bucket, list_files_from_bucket

from simple_term_menu import TerminalMenu
from functools import wraps
import logging
import pandas as pd

LOGGING_FORMAT = "%(asctime)s||[%(pathname)s:%(lineno)d]||%(levelname)s||%(message)s"
logging.basicConfig(format=LOGGING_FORMAT)
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

try:
    import geopandas as gpd
except ImportError:
    LOG.warn("Geopandas not found, caching a geopandas dataframe will not be possible")


DIR_PATH = os.path.dirname(os.path.realpath(__file__))

DATA_BUCKET = "{{cookiecutter.data_bucket}}"
DATA_BUCKET_FOLDER = os.path.join(
    "{{cookiecutter.data_bucket_folder}}", "{{cookiecutter.repo_name}}"
)


def cacheable(dirname: str = "/.cache", filename: str = None, geo=False):
    def decorator(
        function,
        *args,
        dirname=dirname,
        filename=filename,
        cache=False,
        geo=geo,
        index=False,
        **kwargs,
    ):
        @wraps(function)
        def wrapper(
            *args,
            dirname=dirname,
            filename=filename,
            cache=cache,
            geo=geo,
            index=index,
            **kwargs,
        ):
            clean_kwargs = {
                k: v
                for k, v in kwargs.items()
                if k not in {"filename", "dirname", "cache", "geo", "index"}
            }
            if cache is False:
                return function(*args, **clean_kwargs)
            else:
                if (filename is None) or (dirname is None):
                    raise ValueError("If cache is False, then 'filename' must be set")
                if not os.path.exists(dirname):
                    LOG.info(f"Creating caching folder '{dirname}'")
                    os.makedirs(dirname)
                file = os.path.join(dirname, filename)
                if not os.path.exists(file):
                    output_df = function(*args, **clean_kwargs)
                    if geo:
                        output_df.to_file(file, driver="GeoJSON")
                    else:
                        output_df.to_csv(file, index=index)
                    return output_df
                else:
                    if geo:
                        return gpd.read_file(file)
                    else:
                        return pd.read_csv(file)

        return wrapper

    return decorator


def download():
    cache_zip = os.path.join(DIR_PATH, "cache.zip")
    cache_dir = os.path.join(DIR_PATH, ".cache")
    if os.path.exists(cache_dir) and os.listdir(cache_dir):
        error_message = (
            f"cache folder '.cache' already exists: {os.path.join(DIR_PATH, '.cache')}. "
            "To make sure this is not overwritten,  download has been halted."
        )

        LOG.error(error_message)
        raise ValueError(error_message)

    bucket_files = list_files_from_bucket(DATA_BUCKET, DATA_BUCKET_FOLDER)

    if bucket_files:
        tm = TerminalMenu([f.name for f in bucket_files])
        selection_index = tm.show()
        selected_file = bucket_files[selection_index]
        with open(cache_zip, "wb") as f:
            selected_file.download_to_file(f)
    else:
        LOG.info(
            'No files in folder "{DATA_BUCKET_FOLDER}" of bucket "{DATA_BUCKET}"\n'
            "Use the upload command to load the first set of timestamped cache data"
        )
    unpack_archive(os.path.join(DIR_PATH, "cache.zip"), cache_dir, format="zip")
    LOG.info(f"Successfully unpacked cache to {cache_dir}")
    LOG.info(f"Removing {cache_zip}...")
    os.remove(cache_zip)


def upload():
    datestring = f"{datetime.now():%Y-%m-%d}"
    ziparc = os.path.join(DIR_PATH, datestring)
    make_archive(ziparc, "zip", os.path.join(DIR_PATH, ".cache"))
    upload_file_to_bucket(f"{ziparc}.zip", DATA_BUCKET, DATA_BUCKET_FOLDER)
