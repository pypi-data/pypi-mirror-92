import datetime
from typing import Any, Dict, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.archive_record import ArchiveRecord
from ..models.batch_entity import BatchEntity
from ..models.fields import Fields
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="Batch")


@attr.s(auto_attribs=True)
class Batch:
    """  """

    archive_record: Union[Unset, ArchiveRecord] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    creator: Union[Unset, UserSummary] = UNSET
    entity: Union[Unset, BatchEntity] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    fields: Union[Unset, Fields] = UNSET
    modified_at: Union[Unset, datetime.datetime] = UNSET
    schema: Union[Unset, SchemaSummary] = UNSET
    web_url: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        archive_record: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict()

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.creator, Unset):
            creator = self.creator.to_dict()

        entity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.entity, Unset):
            entity = self.entity.to_dict()

        id = self.id
        name = self.name
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self.modified_at, Unset):
            modified_at = self.modified_at.isoformat()

        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        web_url = self.web_url

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if entity is not UNSET:
            field_dict["entity"] = entity
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if fields is not UNSET:
            field_dict["fields"] = fields
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if schema is not UNSET:
            field_dict["schema"] = schema
        if web_url is not UNSET:
            field_dict["webURL"] = web_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        archive_record: Union[Unset, ArchiveRecord] = UNSET
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = ArchiveRecord.from_dict(cast(Dict[str, Any], _archive_record))

        created_at = None
        _created_at = d.pop("createdAt", UNSET)
        if _created_at is not None:
            created_at = isoparse(cast(str, _created_at))

        creator: Union[Unset, UserSummary] = UNSET
        _creator = d.pop("creator", UNSET)
        if _creator is not None and not isinstance(_creator, Unset):
            creator = UserSummary.from_dict(cast(Dict[str, Any], _creator))

        entity: Union[Unset, BatchEntity] = UNSET
        _entity = d.pop("entity", UNSET)
        if _entity is not None and not isinstance(_entity, Unset):
            entity = BatchEntity.from_dict(cast(Dict[str, Any], _entity))

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if _fields is not None and not isinstance(_fields, Unset):
            fields = Fields.from_dict(cast(Dict[str, Any], _fields))

        modified_at = None
        _modified_at = d.pop("modifiedAt", UNSET)
        if _modified_at is not None:
            modified_at = isoparse(cast(str, _modified_at))

        schema: Union[Unset, SchemaSummary] = UNSET
        _schema = d.pop("schema", UNSET)
        if _schema is not None and not isinstance(_schema, Unset):
            schema = SchemaSummary.from_dict(cast(Dict[str, Any], _schema))

        web_url = d.pop("webURL", UNSET)

        batch = cls(
            archive_record=archive_record,
            created_at=created_at,
            creator=creator,
            entity=entity,
            id=id,
            name=name,
            fields=fields,
            modified_at=modified_at,
            schema=schema,
            web_url=web_url,
        )

        return batch
