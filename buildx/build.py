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
            dockerfile_template_path = os.path.abspath(os.path.join("dockerfiles", f"{language.upper()}_DOCKERFILE"))
            dest_path = os.path.join(source_path, source_code)
            shutil.copy(dockerfile_template_path, os.path.join(dest_path, "Dockerfile"))
        except Exception as e:
            raise e

    @staticmethod
    def buildDockerfile(source_path, source_code):
        source_code_path = os.path.join(source_path, source_code)
        kaniko_command = [
            "/kaniko/executor"
            "--dockerfile=Dockerfile",
            f"--context={source_code_path}",
            f"--destination=172.17.0.2:5000/{source_code}:latest"
        ]

        try:
            result = subprocess.run(
                kaniko_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                check=True,
                text=True
            )
            logging.log(logging.INFO, result.stdout)
        except subprocess.CalledProcessError as e:
            raise e
        return result.stdout


if __name__ == "__main__":
    check_docker_file_exist = ImageBuild.checkDockerfileExist('/tmp', 'code')
    if not check_docker_file_exist:
        ImageBuild.generateDockerfile(source_path='/tmp', source_code='code', language='python')
    ImageBuild.buildDockerfile(source_path='/tmp', source_code='code')
