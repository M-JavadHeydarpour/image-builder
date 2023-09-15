import zipfile
import tarfile
import rarfile
import os


class Initialize:

    @staticmethod
    def extractSourceCode(file_name, file_path):
        extension = file_name[1].lower()
        file_name = file_name[0].lower()

        source_path = file_path + '/' + file_name + '.' + extension
        destination_path = file_path + '/' + file_name
        try:
            if extension == 'zip':
                with zipfile.ZipFile(source_path, 'r') as zip_ref:
                    zip_ref.extractall(destination_path)
            elif extension == 'tar.gz' or extension == 'tgz':
                with tarfile.open(source_path, 'r:gz') as tar_ref:
                    tar_ref.extractall(destination_path)
            elif extension == 'tar':
                with tarfile.open(source_path, 'r') as tar_ref:
                    tar_ref.extractall(destination_path)
            elif extension == 'rar':
                with rarfile.RarFile(source_path, 'r') as rar_ref:
                    rar_ref.extractall(destination_path)
            else:
                raise Exception("File format not allowed")

            return destination_path
        except Exception as e:
            raise e
