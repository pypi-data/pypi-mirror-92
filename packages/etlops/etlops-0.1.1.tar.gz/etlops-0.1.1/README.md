# Etlops

Etlops (ETL Operations) is a set of components that make developing ETL workloads easier.

## Submodules

- **clients**: Wrappers around common relational (MySQL) and MPP databases (Snowflake), as well as cloud storages (S3 and GCP Storage).
- **databseops**: Components to work programmatically with relational and MPP databases like transactions and sequence of queries.
- **streams**: Pending.

## Examples

```python
from etlops.clients.gcpstorage import GCPStorageClient
from etlops.clients.cloudstorage import CloudFile
import os
from datetime import date
from pprint import pprint

g = GCPStorageClient()
​
 # get serialized metadata of all buckets in the project (list of dicts)
pprint(g.list_buckets())
​
 # get serialized metadata of all objects in bucket (list of dicts)
pprint(g.list_bucket_objects("bucket_name"))

# Download a file as string:
cloud_file = CloudFile("object_key_in_bucket", "bucket_name", {gcp_download_mode: "string"})
downloaded_file = g.download(cloud_file)
print(downloaded_file.get_file())

# Download a file as named_file:
cloud_file = CloudFile("object_key_in_bucket", "bucket_name", {gcp_download_mode: "named_file", gcp_downloaded_file_path="path/in/local/filesystem"})
downloaded_file = g.download(cloud_file)
with open("path/in/local/filesystem", 'r') as file:
	print(file.read()) # 'r' or 'rb' depending on file content

# Download a file as file-like:
cloud_file = CloudFile("object_key_in_bucket", "bucket_name", {gcp_download_mode: "file-like", gcp_downloaded_file_path="path/in/local/filesystem"})
downloaded_file = g.download(cloud_file)
downloaded_file.get_file() # returns instance of BufferedWritter (https://docs.python.org/3/library/io.html#io.BufferedWriter)

# Upload a file as string:
cloud_file = CloudFile("object_key_in_bucket", "bucket_name", {gcp_upload_mode: "string"}, "file content")
g.upload(cloud_file)

# Upload a file as named_file:
cloud_file = CloudFile("object_key_in_bucket", "bucket_name", {gcp_upload_mode: "named_file"}, "file content")
g.upload(cloud_file)
cloud_file = CloudFile("object_key_in_bucket", "bucket_name", dict(gcp_upload_mode="named_file", gcp_uploading_file_path="path/to/file/to/be/uploaded"))
g.upload(cloud_file)

# Upload a file as file-like:
cloud_file = CloudFile("object_key_in_bucket", "bucket_name", {gcp_upload_mode: "file-like"}, "file content")
with open("path/to/file/to/be/uploaded", 'rb') as file_handle:
    cloud_file = CloudFile("object_key_in_bucket", "bucket_name", dict(gcp_upload_mode="file-like"))
    cloud_file.set_file(file_handle)
    g.upload(cloud_file)

```

## API Reference

### clients

_class_ `etlops.clients.cloudstorage`.**CloudFile**(bucket_file_path: str, bucket: str, cloud_specific_params: dict = None, file_to_upload=None)

Utility class used to configure upload and download operations on files across different cloud storage systems.

Constructor parameters:

- bucket_file_path: `str` (required): Key of the object in the bucket it is located.
- bucket: `str` (required): ID of the bucket where the object was uploaded.
- cloud_specific_params: `dict` (optional): Parameters to specify the behaviour of the download or upload operation.
- file_to_upload (optional): Binary of the file to be uploaded. To be used only for upload operations. Its setting can be delayed prior to passing an instance of this class to the client's upload method by using the set_file method or also specifying a file path parameter so the client fetches the file from the filesystem.

Attributes

- \_bucket_file_path: `str` = Key of the object in the bucket.
  \_bucket: `str` = ID of the bucket to upload or download the object from.
- \_cloud_specific_params: `dict` = Key-value store of parameters to regulate the download / upload operation.
- \_file = Optional. Actual file to be uploaded if the mode of upload entails uploading a file-like or a string.

Methods

- **get_cloud_specific_param**(parameter: `str`): Returns the parameter value for the specified key (parameter argument).

- **has_cloud_specific_parameter**(parameter: `str`) -> `bool`: Returns True if the parameter exists for this CloudFile, False otherwise.

- **get_bucket_file_path**() ->`str`: Returns the \_bucket_file_path attribute.

- **get_bucket**() -> `str`: Returns the \_bucket attribute.

- **set_file**(file) -> `None`: Sets the file parameter to the \_file attribute.

- **get_file**(): Returns the \_file attribute.

---

_class_ `etlops.clients.gcpstorage`.**GCPStorageClient**()

Wrapper of the GCP Storage client from the google-cloud-storage python SDK. See documentation here:

https://googleapis.dev/python/storage/latest/index.html

Constructor parameters:
None

Attributes

- \_client: Instance of `google.cloud.storage.client.Client`

Methods

- **download**(cloud_file: `etlops.clients.cloudstorage.CloudFile`) -> CloudFile: Returns a CloudFile containing a downloaded file according to the parameters specified in cloud_file.

  You can instantiate the CloudFile class with the following `cloud_specific_params` to configure the download operation:

- `gcp_download_mode`: One of `string`, `named_file` or `file-like`.
- `gcp_bucket_filepath`: Key of the object in the bucket to download the file from.
- `gcp_downloaded_file_path`: Only to be used when `gcp_download_mode ` is `named-file` or `file-like`. Absolute or relative path on the local filesystem to download the file to. In the case of `file-like`, the content of the downloaded file will be written to the file the path points to.

When downloading a file as `file-like`, you have 2 options: - To set `gcp_downloaded_file_path` as a `cloud_specific_parameter`, which will write the downloaded file on a file on that path. - To not set `gcp_downloaded_file_path` as a `cloud_specific_parameter`, which will make available an opened `BufferedWritter` instance in the \_file attribute of the CloudFile instance.

If you downloaded as `string`or `file-like` without specifying a `gcp_downloaded_file_path`. You can access the downloaded file by calling the method `get_file` of CloudFile.

- **upload**(cloud_file: `etlops.clients.cloudstorage.CloudFile`) -> None: Uploads a given CloudFile given according to the parameters specificed in cloud_file.

  You can instantiate the CloudFile class with the following `cloud_specific_params` to configure the download operation:

- `gcp_upload_mode`: One of `string`, `named_file` or `file-like`.
- `gcp_bucket_filepath`: Key of the object in the bucket to download the file from.
- `gcp_uploading_file_path`: Only to be used when `gcp_upload_mode ` is `named-file` or `file-like`. Absolute or relative path on the local filesystem to the file intended to be uploaded

When uploading a file as `file-like`, you have 2 options: - To set `gcp_uploading_file_path` as a `cloud_specific_parameter`, which will make the file that paths points to be read and uploaded. - To not set `gcp_uploading_file_path` as a `cloud_specific_parameter` and setting explicitly the file to be uploaded calling the `set_file` on the CloudFile instance.

- **list_buckets**() -> `list`: Returns a list of `google.cloud.storage.bucket.Bucket` instances for the authenticated service account provided by the environment variable`GOOGLE_APPLICATION_CREDENTIALS`.

- **get_bucket**(bucket_id: `str`) -> `google.cloud.storage.bucket.Bucket`: Returns an instance of `google.cloud.storage.bucket.Bucket` matching the provided `bucket_id`.

- **list_bucket_objects**(bucket_id: `str`) -> list: Returns a list of `google.cloud.storage.blob.Blob` instances stored in the provided `bucket_id`.

- **build_object**(bucket_file_path: `str`, bucket_name: `str`) -> `google.cloud.storage.Blob`: Returns an instance of `google.cloud.storage.Blob` matching the given `bucket_name` and `bucket_file_path`.

---

_class_ `etlops.clients.awss3`.**AWSS3Client**()

Wrapper of the AWS S3 client from the boto3 python SDK. See documentation here:

https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

Constructor parameters:
None

Attributes

- \_client: Instance of `boto3.resources.factory.s3.ServiceResource`

Methods

- **download**(cloud_file: `etlops.clients.cloudstorage.CloudFile`) -> CloudFile: Returns a CloudFile containing a downloaded file according to the parameters specified in cloud_file.

  You can instantiate the CloudFile class with the following `cloud_specific_params` to configure the download operation:

- `gcp_download_mode`: Either `file-like` or `named_file`.
- `gcp_bucket_filepath`: Key of the object in the bucket to download the file from.
- `gcp_downloaded_file_path`: Absolute or relative path on the local filesystem to download the file to. In the case of `file-like`, the content of the downloaded file will be written to the file the path points to.

When downloading a file as `file-like`, you have 2 options: - To set `gcp_downloaded_file_path` as a `cloud_specific_parameter`, which will write the downloaded file on a file on that path. - To not set `gcp_downloaded_file_path` as a `cloud_specific_parameter`, which will make available an opened `BufferedWritter` instance in the \_file attribute of the CloudFile instance.

If you downloaded as `file-like` without specifying a `gcp_downloaded_file_path`. You can access the downloaded file by calling the method `get_file` of CloudFile.

- **upload**(cloud_file: `etlops.clients.cloudstorage.CloudFile`) -> None: Uploads a given CloudFile given according to the parameters specificed in cloud_file.

  You can instantiate the CloudFile class with the following `cloud_specific_params` to configure the download operation:

- `gcp_upload_mode`: Either `named_file` or `file-like`.
- `gcp_bucket_filepath`: Key of the object in the bucket to download the file from.
- `gcp_uploading_file_path`: Absolute or relative path on the local filesystem to the file intended to be uploaded.

When uploading a file as `file-like`, you have 2 options: - To set `gcp_uploading_file_path` as a `cloud_specific_parameter`, which will make the file that paths points to be read and uploaded. - To not set `gcp_uploading_file_path` as a `cloud_specific_parameter` and setting explicitly the file to be uploaded calling the `set_file` on the CloudFile instance.

- **list_buckets**() -> `list`: Returns a list of `dict` containing basic metadata of the buckets present in the authenticated account. To switch accounts, check https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html. Remember that you can set an alternative \_client attribute after instantiating this class.
  Contained metadata in the `dict`instances:

  - `bucket_id`: ID of the bucket.
  - `created_at`: Timestamp (UTC) when the bucket was created.

- **get_bucket**(bucket_id: `str`) -> `boto3.resources.factory.s3.Bucket`: Returns an instance of `boto3.resources.factory.s3.Bucket` matching the provided `bucket_id`.

- **list_bucket_objects**(bucket_id: `str`) -> list: Returns a list of `dict` containing basic metadata of the objects stored in the provided `bucket_id`.
  Contained metadata in the `dict`instances:

  - `object_key`: Key of the object in the bucket it is located.
  - `bucket_id`: ID of the bucket where the object was uploaded.
  - `created_at`: Timestamp (UTC) when the object was uploaded.

- **build_object**(bucket_file_path: `str`, bucket_name: `str`) -> `boto3.resources.factory.s3.Object`: Returns an instance of `boto3.resources.factory.s3.Object` matching the given `bucket_name` and `bucket_file_path`.

## Development

To develop on the `etlops` library, the following is required:

- Black formatting
- Adding unit / integration tests where appropriate

### Code Style

The code style is [black](https://github.com/psf/black). All code should be run through the latest version of `black` to ensure code formatting consistency and minimal git diffs during changes. It is highly recommended to set up your editor to have `black` run every time you save a file.

### Testing

#### Setting Up Your Test Environment
All unit tests, by default, can be run by simply cloning the project. However, in order to run integration tests, credential values must be supplied. In order to do this, first copy the `.env.example` file, rename it to `.env`, and populate all of the values as listed in the example. These values are automatically injected into the test environment so that the integration tests can utilize them.

#### Executing the Tests

Etlops uses `pytest` to run and test our code. To run the entire test suite, including integration tests, simply run

```bash
$ pytest
```

We mark integration tests with a pytest marker, `integration`. To run _only_ the integration tests, pytest can be invoked as:

```bash
$ pytest -m integration
```

Inversely, to run all tests _but_ integration tests, pytest can be invoked as:

```bash
$ pytest -m "not integration".
```

#### Marking Tests

While we have a separate `tests/integration` directory, `pytest` needs a way of knowing these are the integration tests. While each test could individually be marked with the `@pytest.mark.integration` decorator, the simpler method is to specify the global `pytestmark` variable. At the top of any file containing integration tests, the line:

```python
pytestmark = pytest.mark.integration
```

should be present.
