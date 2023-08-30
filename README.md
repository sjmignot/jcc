# Cookiecutter Notebook Scaffold

A scaffold for a simple data analysis notebook.

This scaffold provides a template for creating a straightforward data analysis notebook.

The notebook includes useful tools for depency management through docker and easy downloading or uploading of cached datasets to Google Cloud Platform (GCP) so that the exact same analysis can be rerun on the exact same data.

## Use this scaffold

This scaffold can be pulled using cookiecutter

```sh
cookiecutter git+ssh://git@github.com/sjmignot/jcookie
```

## Running the notebook in docker

This notebook also allows the notebook to be run in jupyter. This builds a docker container with the necessary dependencies and then tries to open
Chrome as an application with the notebook.

```sh
poery run dj
```

## Taking advantage of caching for mutable or big datasets

To take advantage of caching for read or processed dataframes, which then lets the data state by saved to GCP, wrap data pulling steps in functions and use the @cacheable decorator on those functions. This will save everything to a .cache dir. For example:

```python
from utils import cacheable

@cacheable('cached_processed.parquet')
def process_data():
	df = pd.read_gbq('SELECT \* FROM `large_mutable_dataset.data`')
	return df
```

Note, doing this means that rerunning the notebook will read from a local file in the cache directory instead of reading from bigquery.

Additionally, the local cache folder can be uploaded to GCP and then redownloaded (by you or someone else) by calling poetry run upload_cache and poetry run download_cache, respectively, in your terminal.

> **Note**
>
> To clear the cache (to pull fresh data, for instance), the cache folder needs to be removed.
