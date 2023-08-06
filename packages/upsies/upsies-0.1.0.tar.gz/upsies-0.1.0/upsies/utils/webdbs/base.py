"""
Abstract base class for online databases
"""

import abc
import asyncio


class WebDbApiBase(abc.ABC):
    """
    Base class for all web DB APIs

    Because not all DBs provide all information, methods that take an `id`
    argument may raise :class:`NotImplementedError`.
    """

    @property
    @abc.abstractmethod
    def name(self):
        """Unique name of this DB"""

    @property
    @abc.abstractmethod
    def label(self):
        """User-facing name of this DB"""

    @abc.abstractmethod
    async def search(self, query):
        """
        Search DB

        :param query: :class:`~.common.Query` instance

        :return: List of :class:`~.common.SearchResult` instances
        """

    @abc.abstractmethod
    async def cast(self, id):
        """Return list of cast names"""

    @abc.abstractmethod
    async def countries(self, id):
        """Return list of country names"""

    @abc.abstractmethod
    async def keywords(self, id):
        """Return list of keywords, e.g. genres"""

    @abc.abstractmethod
    async def summary(self, id):
        """Return short plot description"""

    @abc.abstractmethod
    async def title_english(self, id):
        """Return English title if different from original title or empty string"""

    @abc.abstractmethod
    async def title_original(self, id):
        """Return original title (e.g. non-English) or empty string"""

    @abc.abstractmethod
    async def type(self, id):
        """Return :class:`~.utils.ReleaseType`"""

    @abc.abstractmethod
    async def year(self, id):
        """Return release year or empty string"""

    async def gather(self, id, *methods):
        """
        Fetch information concurrently

        :param id: Valid ID for this DB
        :param methods: Names of coroutine methods of this class
        :type methods: sequence of :class:`str`

        :return: Dictionary that maps `methods` to return values
        """
        corofuncs = (getattr(self, method) for method in methods)
        awaitables = (corofunc(id) for corofunc in corofuncs)
        results = await asyncio.gather(*awaitables)
        # "The order of result values corresponds to the order of awaitables in `aws`."
        # https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently
        return {method: result for method, result in zip(methods, results)}
