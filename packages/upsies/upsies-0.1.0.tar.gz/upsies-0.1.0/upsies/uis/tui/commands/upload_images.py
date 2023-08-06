"""
Upload images to image hosting service
"""

from .... import jobs, utils
from .base import CommandBase


class upload_images(CommandBase):
    """Upload images to image hosting service"""

    names = ('upload-images', 'ui')

    argument_definitions = {
        'IMAGEHOST': {
            'type': utils.types.imghost,
            'help': ('Case-insensitive name of image hosting service\n'
                     'Supported services: ' + ', '.join(utils.types.IMGHOST_NAMES)),
        },
        'IMAGE': {
            'nargs': '+',
            'help': 'Path to image file',
        },
    }

    @utils.cached_property
    def jobs(self):
        return (
            jobs.imghost.ImageHostJob(
                ignore_cache=self.args.ignore_cache,
                imghost=utils.imghosts.imghost(
                    name=self.args.IMAGEHOST,
                    **self.config['imghosts'][self.args.IMAGEHOST],
                ),
                enqueue=self.args.IMAGE,
            ),
        )
