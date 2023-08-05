import abc
from typing import Any, List, Optional, Tuple, Type, overload, Literal, Union

from .models import (
    DBIndex,
    DeleteResult,
    DocumentDBModel,
    FireOffset,
    SortOrder,
    WhereCondition,
    WriteResult,
)


class BaseClient(abc.ABC):
    @abc.abstractmethod
    def generate_id(self, collection_name: str) -> str:
        pass

    @abc.abstractmethod
    async def insert(
        self, model: DocumentDBModel, include=None, exclude=None, session: Any = None,
    ) -> WriteResult:
        pass

    @abc.abstractmethod
    async def count(self, model: Type[DocumentDBModel], session: Any = None) -> int:
        pass

    @abc.abstractmethod
    async def get_dict(
        self, collection_name: str, _id: str, session: Any = None,
    ) -> Optional[dict]:
        pass

    @abc.abstractmethod
    async def get(
        self, model: Type[DocumentDBModel], _id: str, session: Any = None,
    ) -> Optional[DocumentDBModel]:
        pass

    @abc.abstractmethod
    async def list_dict(
        self,
        collection_name: str,
        where: List[WhereCondition] = [],
        _limit: int = 0,
        _sort: List[Tuple[str, SortOrder]] = None,
        mongo_offset: int = 0,
        fire_offset: FireOffset = None,
    ) -> List[dict]:
        pass

    @abc.abstractmethod
    async def list(
        self,
        model: Type[DocumentDBModel],
        where: List[WhereCondition] = [],
        _limit: int = 0,
        _sort: List[Tuple[str, SortOrder]] = None,
        mongo_offset: int = 0,
        fire_offset: FireOffset = None,
    ) -> List[DocumentDBModel]:
        """
        List documents in a collection based on specified conditions, note this interface is limiting
        query to the smaller set of features (currently Firestore).

        Arguments:
            model {DocumentDBModel} -- [description]

        Keyword Arguments:
            where {List[WhereCondition]} -- [description] (default: {[]})
            session {Any} -- [description] (default: {None})
            _offset {int} -- [description] (default: {0})
            _limit {int} -- [description] (default: {0})
            _sort {List[Tuple} -- [description] (default: {None})

        Returns:
            Cursor -- [description]
        """
        pass

    @abc.abstractmethod
    async def delete(
        self, model: Type[DocumentDBModel], _id: str, session: Any = None
    ) -> DeleteResult:
        pass

    @abc.abstractmethod
    async def update_one(
        self, model: Type[DocumentDBModel], id: str, data: dict, session: Any = None,
    ) -> WriteResult:
        pass

    @abc.abstractmethod
    async def create_indexes(self, index=List[DBIndex]) -> Optional[List[str]]:
        pass

    @abc.abstractmethod
    async def find_one_dict(
        self,
        collection_name: str,
        where: List[WhereCondition] = [],
        session: Any = None,
    ) -> Optional[dict]:
        pass

    @abc.abstractmethod
    async def find_one(
        self,
        model: Type[DocumentDBModel],
        where: List[WhereCondition] = [],
        session: Any = None,
    ) -> Optional[DocumentDBModel]:
        pass

    # FIXME: Need to add this back once it has been fixed
    # @abc.abstractmethod
    # async def update_many(
    #     self, model: Type[DocumentDBModel], data: List[Tuple[str, dict]]
    # ) -> WriteResult:
    #     pass
