import click

from .processor import AssetFetcher, Creative, FetchMode, zip_images
from ..settings import AWS_BUCKET, AWS_REGION


@click.command(help='Get the manifest from a url.')
@click.argument('url')
@click.option('-f', '--filename', default='out',
              help='Name of Zip File to output.')
@click.option('-m', '--mode', type=click.Choice([e.value for e in FetchMode], case_sensitive=False),
              default=FetchMode.HTTP.value, help='Mode of Download (http or aws).')
@click.option('-b', '--bucket', default=AWS_BUCKET,
              help='Optional bucket path')
@click.option('-r', '--region', default=AWS_REGION,
              help='Optional region')
def build_image_from_manifest(url, filename, mode, bucket, region):
    """Using the specified URL location, will retrieve, process manifest and write image to zip.

    Parameters:
        url (str):
            The location of the manifest to download and build image from.
        filename (str):
            The filename of the final zip file to generate.
        mode (str):
            If we are retrieving the manifest from http or aws.
        bucket (str):
            The name of the bucket where the file is stored.
        region (str):
            The region of the bucket where the file is stored.
    """
    client = AssetFetcher(mode.upper(), bucket, region)

    creative = Creative(url, client)

    generated_image = creative.render()
    click.echo("Image Generated!")

    zip_images(generated_image, filename=filename)
    click.echo(f"Image Now Available in {filename}.zip")
