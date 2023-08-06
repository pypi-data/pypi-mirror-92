from coegil.ApiService import set_configuration, api_get, api_save, get_environment
from coegil.Helpers import put_s3_object
import tempfile
import subprocess
import sys
import tarfile
import os
import click


@click.group()
def cli():
    pass


@cli.command('configure', help="Configure your environment.")
@click.option('--key', prompt=True, hide_input=True, required=True, help="Your Coegil API key.")
@click.option('--env', required=False, default='prod', help="Optionally, set an environment.  "
                                                            "If you don't know what this is, leave it blank.")
def configure(key: str, env: str):
    set_configuration(env, key)


@cli.command('validate', help="Validate your environment.")
def validate():
    result = api_get('/public/management/key/validate', {})
    environment = get_environment()
    if environment != 'prod':
        result['environment'] = environment
    print(result)


@cli.command('publish', help="Publish a python library to an asset.")
@click.option('--asset_id', required=True, help="The asset's unique identifier.")
@click.option('--package_name', required=True, help="Your package's desire name.")
@click.option('--library', required=True, type=click.Path(exists=True),
              help="The location of the Python library to package.")
def publish(asset_id: str, package_name: str, library: str):
    with tempfile.TemporaryDirectory() as wheel_destination:
        commands = [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            library,
            f'--wheel-dir={wheel_destination}'
        ]
        process = subprocess.Popen(commands, stderr=subprocess.PIPE)
        out, err = process.communicate()
        output = out.decode() if out is not None else ''
        error = err.decode()
        success = error == ''
        print(output)
        if not success:
            raise Exception(error)
        tar_file_name = os.path.join(wheel_destination, f'{package_name}.tar')
        with tarfile.open(tar_file_name, "w:gz") as tar:
            tar.add(wheel_destination, arcname=os.path.basename(wheel_destination))

        s3_credentials = api_get('/public/artifact/credentials', {
            'asset_id': asset_id,
            'artifact_name': package_name,
            'artifact_sub_type': 'python_package'
        })
        s3_bucket = s3_credentials['Bucket']
        s3_key = s3_credentials['Key']
        artifact_id = s3_credentials['ArtifactGuid']
        credential_override = s3_credentials['Credentials']
        with open(tar_file_name, 'rb') as package:
            put_s3_object(s3_bucket, s3_key, package, credential_override=credential_override)
        api_save('POST', '/public/artifact', {
            'asset_id': asset_id,
            'artifacts': [{
                'artifact_name': package_name,
                'artifact_type': 'S3',
                'artifact_sub_type': 'python_package',
                'artifact_id': artifact_id
            }]
        })


if __name__ == '__main__':
    cli()
