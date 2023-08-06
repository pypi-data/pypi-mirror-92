"""
Abstract base class for jobs
"""

import abc
import asyncio
import collections
import json
import os
import re

from ..utils import cached_property, fs, signal

import logging  # isort:skip
_log = logging.getLogger(__name__)


class JobBase(abc.ABC):
    """
    Base class for all jobs

    :param str home_directory: Directory that is used to store files and cache
        output
    :param str ignore_cache: Whether cached output and previously created files
        should not be re-used
    :param bool hidden: Whether to hide the job's output in the UI
    :param bool autostart: Whether this job is started automatically

    Any additional keyword arguments are passed on to :meth:`initialize`.

    If possible, arguments should be validated before creating a job to fail
    early when sibling jobs haven't started doing work that has to be cancelled
    in case of error.

    Methods and properties of jobs should not raise any expected exceptions.
    Exceptions should instead be passed to :meth:`error` (report message to
    user) or to :meth:`exception` (throw traceback at user), and the job should
    :meth:`finish` immediately with an :attr:`exit_code` `> 0`.
    """

    @property
    @abc.abstractmethod
    def name(self):
        """Internal name (e.g. for the cache file name)"""

    @property
    @abc.abstractmethod
    def label(self):
        """User-facing name"""

    @property
    def home_directory(self):
        """
        Directory that is used to store files

        Cached output is stored in a subdirectory called ".output".
        """
        return self._home_directory

    @property
    def ignore_cache(self):
        """Whether cached output and previously created files should not be re-used"""
        return self._ignore_cache

    @property
    def hidden(self):
        """Whether to hide this job's output in the UI"""
        return self._hidden

    @property
    def autostart(self):
        """
        Whether this job is started automatically

        This property is not used by this class itself. It is only a flag that
        is supposed to be evaluated by any job starting facilities.

        If this value is falsy, :meth:`start` must be called manually.
        """
        return self._autostart

    @property
    def kwargs(self):
        """Keyword arguments from instantiation as :class:`dict`"""
        return self._kwargs

    @property
    def signal(self):
        """
        :class:`~.signal.Signal` instance

        The following signals are added by the base class. Subclasses can add
        their own signals.

        ``finished``
            is emitted when :meth:`finish` is called or when output is read from
            cache. Registered callbacks get no arguments.

        ``output``
            is emitted when :meth:`send` is called or when output is read from
            cache. Registered callbacks get the value passed to :meth:`send` as
            a positional argument.

        ``error``
            is emitted when :meth:`error` is called. Registered callbacks get
            the value passed to :meth:`error` as a positional argument.
        """
        return self._signal

    def __init__(self, *, home_directory=None, ignore_cache=False, hidden=False,
                 autostart=True, **kwargs):
        if home_directory:
            # Custome home specific to some content. Store cache in hidden
            # directory in there.
            self._home_directory = str(home_directory)
            self._cache_directory = os.path.join(self._home_directory, '.cache')
        else:
            # Default home, something like /tmp/upsies. We want to store files
            # and cache in the same directory.
            self._home_directory = fs.tmpdir()
            self._cache_directory = self.home_directory
        self._ignore_cache = bool(ignore_cache)
        self._hidden = bool(hidden)
        self._autostart = bool(autostart)
        self._is_started = False
        self._exception = None
        self._errors = []
        self._output = []
        self._signal = signal.Signal('output', 'error', 'finished')
        self._signal.register('output', lambda output: self._output.append(str(output)))
        self._signal.register('error', lambda error: self._errors.append(error))
        self._signal.record('output')
        self._finished_event = asyncio.Event()
        self._kwargs = kwargs
        self.initialize(**kwargs)

    def initialize(self):
        """
        Called by :meth:`__init__` with additional keyword arguments

        This method should handle its arguments and return quickly.
        """

    def execute(self):
        """
        Do the job, e.g. prompt for user input or start background worker

        This method must not block.
        """

    def start(self):
        """
        Called by the main entry point when this job is executed

        If there is cached output available, load it and call :meth:`finish`.
        Otherwise, call :meth:`execute`.

        :raise RuntimeError: if this method is called multiple times or if
            reading from cache file fails unexpectedly
        """
        if self._is_started:
            raise RuntimeError('start() was already called')
        else:
            self._is_started = True

        try:
            cache_was_read = self._read_cache()
        except BaseException:
            self.finish()
            raise

        if cache_was_read:
            self.finish()
        else:
            _log.debug('Executing %r', self)
            self.execute()

    async def wait(self):
        """
        Wait for this job to finish

        Subclasses that need to wait for I/O should do so by overriding this
        method.

        Subclasses must call the parent's method (``super().wait()``).

        This method returns when :meth:`finish` is called.

        :attr:`is_finished` is `False` before this method returns and `True`
        afterwards.

        Calling this method multiple times simultaneously is safe.

        :raise: Any exceptions given to :meth:`exception`
        """
        await self._finished_event.wait()
        if self._exception is not None:
            raise self._exception

    def finish(self):
        """
        Cancel this job if it is not finished yet and emit ``finished`` signal

        Calling this method unblocks any calls to :meth:`wait`.

        :attr:`is_finished` is `True` after this method was called.

        Calling this method multiple times simultaneously is safe.

        Subclasses must call the parent's method (``super().finish()``).

        This method does not block.
        """
        if not self.is_finished:
            self._finished_event.set()
            self.signal.emit('finished')
            self._write_cache()

    @property
    def is_finished(self):
        """Whether :meth:`finish` was called"""
        return self._finished_event.is_set()

    @property
    def exit_code(self):
        """`0` if job was successful, `> 0` otherwise, None while job is not finished"""
        if self.is_finished:
            if not self.output or self.errors or self._exception:
                return 1
            else:
                return 0

    @property
    def output(self):
        """Result of this job as an immutable sequence of strings"""
        return tuple(self._output)

    @property
    def info(self):
        """
        Additional information that is only displayed in the UI and not part of the
        job's result
        """
        return ''

    def send(self, output):
        """Append `output` to :attr:`output` and emit ``output`` signal"""
        if not self.is_finished:
            if output:
                self.signal.emit('output', str(output))

    @property
    def errors(self):
        """Sequence of reported errors (strings or exceptions)"""
        return tuple(self._errors)

    def clear_errors(self):
        """Empty :attr:`errors`"""
        if not self.is_finished:
            self._errors.clear()

    def error(self, error, finish=False):
        """
        Append `error` to :attr:`errors` and emit ``error`` signal

        :param bool finish: Whether to call :meth:`finish` after handling
            `error`
        """
        if not self.is_finished:
            if finish:
                self.finish()
            self.signal.emit('error', error)

    def exception(self, exception):
        """
        Set exception to raise in :meth:`wait` and call :meth:`finish`

        .. warning:: Setting an exception means you want to throw a traceback in
                     the user's face, which may not be a good idea.

        :param Exception exception: Exception instance
        """
        if not self.is_finished:
            import traceback
            tb = ''.join(traceback.format_exception(
                type(exception), exception, exception.__traceback__))
            _log.debug('Exception in %s: %s', self.name, tb)
            self._exception = exception
            self.finish()

    def _write_cache(self):
        """
        Store :attr:`output` in :attr:`cache_file`

        The base class implementation stores output as JSON. Child classes may
        use other formats.

        :raise RuntimeError: if :attr:`output` is not JSON-encodable or
            :attr:`cache_file` is not writable
        """
        if self.output and self.exit_code == 0 and self.cache_file:
            emissions_string = json.dumps(self.signal.emissions, indent=4)
            try:
                with open(self.cache_file, 'w') as f:
                    f.write(emissions_string)
                    f.write('\n')
            except OSError as e:
                if e.strerror:
                    raise RuntimeError(f'Unable to write cache {self.cache_file}: {e.strerror}')
                else:
                    raise RuntimeError(f'Unable to write cache {self.cache_file}: {e}')

    def _read_cache(self):
        """
        Set :attr:`output` to data stored in :attr:`cache_file`

        :raise RuntimeError: if :attr:`cache_file` exists and is unreadable

        :return: `True` if cache file was read, `False` otherwise
        """
        if not self._ignore_cache and self.cache_file and os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    emissions_string = f.read()
            except OSError as e:
                if e.strerror:
                    raise RuntimeError(f'Unable to read cache {self.cache_file}: {e.strerror}')
                else:
                    raise RuntimeError(f'Unable to read cache {self.cache_file}: {e}')
            else:
                emissions = json.loads(emissions_string)
                _log.debug('%s: Replaying cached signals: %r', self.name, emissions)
                self.signal.replay(emissions)
                return True
        return False

    @cached_property
    def cache_directory(self):
        """Path to existing directory that stores cache files"""
        if not os.path.exists(self._cache_directory):
            os.mkdir(self._cache_directory)
        return self._cache_directory

    @cached_property
    def cache_file(self):
        """
        File path in :attr:`cache_directory` to store cached :attr:`output` in

        If this property returns `None`, cache is not read or written.
        """
        cache_id = self.cache_id
        if cache_id is None:
            return None
        elif not cache_id:
            filename = f'{self.name}.json'
        else:
            # Avoid file name being too long. 255 bytes seems common. Leave
            # some headroom for multibytes.
            # https://en.wikipedia.org/wiki/Comparison_of_file_systems#Limits
            max_len = 250 - len(self.name) - len('..json')
            cache_id_str = self._cache_data_as_string(cache_id)
            if len(cache_id_str) > max_len:
                cache_id_str = ''.join((
                    cache_id_str[:int(max_len / 2 - 1)],
                    '…',
                    cache_id_str[-int(max_len / 2 - 1):],
                ))
            if cache_id_str:
                filename = f'{self.name}.{cache_id_str}.json'
            else:
                filename = f'{self.name}.json'
            filename = fs.sanitize_filename(filename)
        return os.path.join(self.cache_directory, filename)

    @cached_property
    def cache_id(self):
        """
        Unique object based on the job's input data

        The return value is turned into a string. Items of non-string iterables
        are passed to :class:`str` and :meth:`~.str.join`\\ ed with ",".

        If this property returns `None`, cache is not read or written.

        The default implementation uses the arguments passed to
        :meth:`initialize`.
        """
        # Check if any values don't have a string representation to prevent
        # random cache IDs
        no_str_regex = re.compile(r'^<[\w\.]+ object at 0x[a-f\d]+>$')
        for key, value in self.kwargs.items():
            if no_str_regex.search(str(key)):
                raise RuntimeError(f'{type(key)!r} has no string representation')
            elif no_str_regex.search(str(value)):
                raise RuntimeError(f'{type(value)!r} has no string representation')
        return self._kwargs

    def _cache_data_as_string(self, value):
        if isinstance(value, collections.abc.Mapping):
            return ','.join((f'{k}={self._cache_data_as_string(v)}' for k, v in value.items()))

        elif isinstance(value, collections.abc.Iterable) and not isinstance(value, str):
            return ','.join((self._cache_data_as_string(v) for v in value))

        elif isinstance(value, (str, os.PathLike)) and os.path.exists(value):
            # Use same cache file for absolute and relative paths
            return str(os.path.realpath(value))

        else:
            return str(value)


class QueueJobBase(JobBase):
    """
    Subclass of :class:`JobBase` with an :class:`asyncio.Queue`

    This job is used to process input asynchronously, e.g. from another job. For
    example, :meth:`enqueue` from :class:`~.jobs.imghost.ImageHostJob` can be
    connected to the ``output`` :class:`~.utils.signal.Signal` of
    :class:`~.jobs.screenshots.ScreenshotsJob`.

    It's also possible to use this job conventionally by passing a sequence of
    values as the `enqueue` argument. This processes all values and finishes the
    job without waiting for more.

    The :meth:`initialize` method of subclasses must accept `enqueue` as a
    keyword argument.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._queue = asyncio.Queue()
        self._read_queue_task = None
        self._enqueue_args = kwargs.get('enqueue', ())

    def execute(self):
        self._read_queue_task = asyncio.ensure_future(self._read_queue())
        if self._enqueue_args:
            for value in self._enqueue_args:
                self.enqueue(value)
            self.finalize()

    async def _read_queue(self):
        while True:
            value = await self._queue.get()
            if self.is_finished:
                raise RuntimeError(f'{type(self).__name__} is already finished')
            elif value is None:
                break
            else:
                await self._handle_input(value)
        self.finish()

    @abc.abstractmethod
    async def _handle_input(self, value):
        """Handle `value` from queue"""

    def enqueue(self, value):
        """Put `value` in queue"""
        self._queue.put_nowait(value)

    def finalize(self):
        """Finish after all currently queued values are handled"""
        self._queue.put_nowait(None)

    def finish(self):
        """
        Stop reading from queue

        Unlike :meth:`JobBase.finish`, this does not finish the job. The job is
        not finished until :meth:`wait` returns.
        """
        if self._read_queue_task:
            self._read_queue_task.cancel()
        super().finish()

    async def wait(self):
        """Wait for internal queue reading task and finish job"""
        if self._read_queue_task:
            try:
                await self._read_queue_task
            except asyncio.CancelledError:
                pass
        await super().wait()
