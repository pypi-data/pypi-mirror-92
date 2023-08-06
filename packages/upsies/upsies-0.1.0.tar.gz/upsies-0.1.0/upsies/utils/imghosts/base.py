"""
Base class for image uploaders
"""

import abc
import json
import os

from .. import fs
from . import common

import logging  # isort:skip
_log = logging.getLogger(__name__)


class ImageHostBase(abc.ABC):
    """
    Base class for image uploaders

    :param str cache_dir: Where to store URLs in JSON files; defaults to the
        return value of :func:`.utils.fs.tmpdir`
    """

    def __init__(self, cache_directory=None):
        self._cache_dir = cache_directory or fs.tmpdir()

    @property
    @abc.abstractmethod
    def name(self):
        """Name of the image hosting service"""

    @property
    def cache_directory(self):
        """Path to directory where upload info is cached"""
        return self._cache_dir

    @cache_directory.setter
    def cache_directory(self, directory):
        self._cache_dir = directory

    async def upload(self, image_path, cache=True):
        """
        Upload image to gallery

        :param str image_path: Path to image file
        :param bool cache: Whether to attempt to get the image URL from cache or
            cache it

        :raise RequestError: if the upload fails

        :return: :class:`~.imghost.common.UploadedImage`
        """
        info = self._get_info_from_cache(image_path) if cache else {}
        if not info:
            info = await self._upload(image_path)
            _log.debug('Uploaded %r: %r', image_path, info)
            self._store_info_to_cache(image_path, info)
        if 'url' not in info:
            raise RuntimeError(f'Missing "url" key in {info}')
        return common.UploadedImage(**info)

    @abc.abstractmethod
    async def _upload(self, image_path):
        """
        Upload a single image

        :param str image_path: Path to an image file

        :return: Dictionary that must contain an "url" key
        """

    def _get_info_from_cache(self, image_path):
        cache_file = self._cache_file(image_path)
        if os.path.exists(cache_file):
            _log.debug('Already uploaded: %s', cache_file)
            try:
                with open(cache_file, 'r') as f:
                    return json.loads(f.read())
            except (OSError, ValueError):
                # We'll overwrite the corrupted cache file later
                pass

    def _store_info_to_cache(self, image_path, info):
        cache_file = self._cache_file(image_path)
        try:
            json_string = json.dumps(info, indent=4) + '\n'
        except (TypeError, ValueError) as e:
            raise RuntimeError(f'Unable to write cache {cache_file}: {e}')

        try:
            with open(cache_file, 'w') as f:
                f.write(json_string)
        except (OSError, TypeError, ValueError) as e:
            msg = e.strerror if getattr(e, 'strerror', None) else e
            raise RuntimeError(f'Unable to write cache {cache_file}: {msg}')

    def _cache_file(self, image_path):
        # If image is in our cache_dir, the image's file name makes it
        # unique. This is usually the case when we're uploading screenshots. If
        # image is not in our cache_dir, use the absolute path as a unique
        # identifier.
        if os.path.dirname(image_path) == self._cache_dir:
            image_path = os.path.basename(image_path)
        else:
            image_path = os.path.abspath(image_path)
        # Max file name length is ususally 255 bytes
        filename = fs.sanitize_filename(image_path[-200:]) + f'.{self.name}.json'
        return os.path.join(self._cache_dir, filename)
