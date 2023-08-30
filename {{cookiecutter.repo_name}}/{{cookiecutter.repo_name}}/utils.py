import os
import pathlib
from functools import wraps
import pandas as pd
import logging
from google.cloud import storage

LOGGING_FORMAT = "%(asctime)s||{%(pathname)s:%(lineno)d}||%(levelname)s||%(message)s"
RECOGNIZED_FILE_EXTENSIONS = {
    "pqt": "parquet",
}

logging.basicConfig(format=LOGGING_FORMAT)
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

try:
    import geopandas as gpd
except ImportError:
    LOG.warn("Geopandas not found, caching a geopandas dataframe will not be possible")


def bucket_exists(bucket_name, client=None):
    client = client or storage.Client()

    bucket = client.get_bucket(bucket_name)
    be = bucket.exists()
    return bucket if be else False


def list_files_from_bucket(bucket_name, bucket_directory=""):
    client = storage.Client()

    if not (bucket := bucket_exists(bucket_name, client)):
        error_message = f"bucket {bucket} does not exist"
        raise ValueError(error_message)

    return list(bucket.list_blobs(prefix=bucket_directory))


def fetch_file_from_bucket(bucket_name, file_name, blob_name=None, destination=None):
    if destination is None:
        destination = file_name

    if os.path.exists(destination):
        LOG.debug(f"{destination} exists, skipping download from {bucket_name}")
        return

    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob_name = os.path.basename(file_name) if blob_name is None else blob_name
    LOG.info(f"downloading {blob_name} from {bucket_name}")
    blob = bucket.blob(blob_name)
    blob.download_to_filename(destination if destination else file_name)


def cacheable(dirname="/.cache", filename=None, geo=False):
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
                    raise ValueError("If cache is True, then 'filename' must be set")
                if not os.path.exists(dirname):
                    LOG.info(f"Creating caching folder '{dirname}'")
                    os.makedirs(dirname)
                file = os.path.join(dirname, filename)
                extension = pathlib.Path(filename).suffix[1:]
                if not os.path.exists(file):
                    output_df = function(*args, **clean_kwargs)
                    if geo:
                        output_df.to_file(file, driver="GeoJSON")
                    else:
                        breakpoint()
                        if save_method := getattr(output_df, f"to_{extension}", None):
                            save_method(file, index=index)
                        elif save_method := getattr(
                            output_df,
                            f"to_{RECOGNIZED_FILE_EXTENSIONS.get(extension, None)}",
                            None,
                        ):
                            save_method(file, index=index)
                        else:
                            LOG.error(
                                "Could not determine proper pandas saving function for file "
                                f"with extension {extension}."
                            )
                            exit()
                    return output_df
                else:
                    if geo:
                        return gpd.read_file(file)
                    else:
                        if read_method := getattr(pd, f"read_{extension}", None):
                            return read_method(file)
                        elif read_method := getattr(
                            pd,
                            f"read_{RECOGNIZED_FILE_EXTENSIONS[extension]}",
                            None,
                        ):
                            return read_method(file)
                        else:
                            LOG.error(
                                "Could not determine proper pandas reading function for file "
                                f"with extension {extension}."
                            )
                            exit()

        return wrapper

    return decorator
