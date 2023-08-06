from typing import Any, Dict, Type, TypeVar, Union, cast

import attr

from ..models.fields import Fields
from ..models.location_archive_record import LocationArchiveRecord
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="Location")


@attr.s(auto_attribs=True)
class Location:
    """  """

    id: str
    barcode: str
    created_at: str
    creator: UserSummary
    fields: Fields
    modified_at: str
    name: str
    parent_storage_id: str
    schema: SchemaSummary
    web_url: str
    archive_record: Union[Unset, None, LocationArchiveRecord] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        barcode = self.barcode
        created_at = self.created_at
        creator = self.creator.to_dict()

        fields = self.fields.to_dict()

        modified_at = self.modified_at
        name = self.name
        parent_storage_id = self.parent_storage_id
        schema = self.schema.to_dict()

        web_url = self.web_url
        archive_record: Union[None, Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "barcode": barcode,
                "createdAt": created_at,
                "creator": creator,
                "fields": fields,
                "modifiedAt": modified_at,
                "name": name,
                "parentStorageId": parent_storage_id,
                "schema": schema,
                "webURL": web_url,
            }
        )
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        barcode = d.pop("barcode")

        created_at = d.pop("createdAt")

        creator = UserSummary.from_dict(d.pop("creator"))

        fields = Fields.from_dict(d.pop("fields"))

        modified_at = d.pop("modifiedAt")

        name = d.pop("name")

        parent_storage_id = d.pop("parentStorageId")

        schema = SchemaSummary.from_dict(d.pop("schema"))

        web_url = d.pop("webURL")

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = LocationArchiveRecord.from_dict(cast(Dict[str, Any], _archive_record))

        location = cls(
            id=id,
            barcode=barcode,
            created_at=created_at,
            creator=creator,
            fields=fields,
            modified_at=modified_at,
            name=name,
            parent_storage_id=parent_storage_id,
            schema=schema,
            web_url=web_url,
            archive_record=archive_record,
        )

        return location
