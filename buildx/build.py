import logging
import os
import shutil
import subprocess


class ImageBuild:

    @staticmethod
    def checkDockerfileExist(source_path, source_name):
        dockerfile_path = source_path + "/" + source_name + "/" + "Dockerfile"
        return os.path.isfile(dockerfile_path)

    @staticmethod
    def generateDockerfile(source_path, source_code, language):
        try:
            dockerfile_template_path = os.path.abspath(
                os.path.join(
                    "/buildx/dockerfiles",
                    f"{language.upper()}_DOCKERFILE"
                )
            )
            dest_path = os.path.join(source_path, source_code)
            shutil.copy(dockerfile_template_path, os.path.join(dest_path, "Dockerfile"))
        except Exception as e:
            raise e

    @staticmethod
    def buildDockerfile(source_path, source_code):
        source_code_path = os.path.join(source_path, source_code)
        kaniko_command = (
            f"/kaniko/executor --dockerfile={source_code_path}/Dockerfile --context={source_code_path} --destination=127.0.0.1:5000/{source_code}:latest"
        )
        try:
            subprocess.check_output(kaniko_command, shell=True, universal_newlines=True)
        except Exception as e:
            raise e

        return True


if __name__ == "__main__":
    check_docker_file_exist = ImageBuild.checkDockerfileExist('/tmp', 'code')
    if not check_docker_file_exist:
        ImageBuild.generateDockerfile(source_path='/tmp', source_code='code', language='python')
    ImageBuild.buildDockerfile(source_path='/tmp', source_code='code')
