from azure.core.exceptions import (
    ResourceExistsError,
    ResourceNotFoundError
)

from azure.storage.fileshare import (
    ShareServiceClient,
    ShareClient,
    ShareDirectoryClient,
    ShareFileClient
)


# service_client = ShareServiceClient.from_connection_string(connection_string)


def create_file_share(connection_string, share_name):
    try:
        # Create a ShareClient from a connection string
        share_client = ShareClient.from_connection_string(
            connection_string, share_name)

        print("Creating share:", share_name)
        share_client.create_share()

    except ResourceExistsError as ex:
        print("ResourceExistsError:", ex.message)


def upload_local_file(connection_string, local_file_path, share_name, dest_file_path):
    try:
        source_file = open(local_file_path, "rb")
        data = source_file.read()

        # Create a ShareFileClient from a connection string
        file_client = ShareFileClient.from_connection_string(
            connection_string, share_name, dest_file_path)

        print("Uploading to:", share_name + "/" + dest_file_path)
        file_client.upload_file(data)

    except ResourceExistsError as ex:
        print("ResourceExistsError:", ex.message)

    except ResourceNotFoundError as ex:
        print("ResourceNotFoundError:", ex.message)


def create_directory(connection_string, share_name, dir_name):
    try:
        # Create a ShareDirectoryClient from a connection string
        dir_client = ShareDirectoryClient.from_connection_string(
            connection_string, share_name, dir_name)

        print("Creating directory:", share_name + "/" + dir_name)
        dir_client.create_directory()

    except ResourceExistsError as ex:
        print("ResourceExistsError:", ex.message)


def list_files_and_dirs(connection_string, share_name, dir_name):
    try:
        # Create a ShareClient from a connection string
        share_client = ShareClient.from_connection_string(
            connection_string, share_name)

        for item in list(share_client.list_directories_and_files(dir_name)):
            if item["is_directory"]:
                print("Directory:", item["name"])
            else:
                print("File:", dir_name + "/" + item["name"])

    except ResourceNotFoundError as ex:
        print("ResourceNotFoundError:", ex.message)


connection_string = "https://blobretry.file.core.windows.net/webblobdata"


def get_files():
    print(connection_string)
    # list_files_and_dirs(connection_string, "", "./")
