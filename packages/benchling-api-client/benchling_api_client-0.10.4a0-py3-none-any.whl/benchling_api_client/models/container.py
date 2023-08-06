import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.archive_record import ArchiveRecord
from ..models.checkout_record import CheckoutRecord
from ..models.container_content import ContainerContent
from ..models.fields import Fields
from ..models.measurement import Measurement
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="Container")


@attr.s(auto_attribs=True)
class Container:
    """  """

    id: str
    name: str
    barcode: str
    checkout_record: CheckoutRecord
    contents: List[ContainerContent]
    created_at: datetime.datetime
    creator: UserSummary
    fields: Fields
    modified_at: datetime.datetime
    parent_storage_id: str
    parent_storage_schema: SchemaSummary
    schema: SchemaSummary
    volume: Measurement
    web_url: str
    project_id: Optional[str]
    archive_record: Union[Unset, ArchiveRecord] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        barcode = self.barcode
        checkout_record = self.checkout_record.to_dict()

        contents = []
        for contents_item_data in self.contents:
            contents_item = contents_item_data.to_dict()

            contents.append(contents_item)

        created_at = self.created_at.isoformat()

        creator = self.creator.to_dict()

        fields = self.fields.to_dict()

        modified_at = self.modified_at.isoformat()

        parent_storage_id = self.parent_storage_id
        parent_storage_schema = self.parent_storage_schema.to_dict()

        schema = self.schema.to_dict()

        volume = self.volume.to_dict()

        web_url = self.web_url
        archive_record: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict()

        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
                "barcode": barcode,
                "checkoutRecord": checkout_record,
                "contents": contents,
                "createdAt": created_at,
                "creator": creator,
                "fields": fields,
                "modifiedAt": modified_at,
                "parentStorageId": parent_storage_id,
                "parentStorageSchema": parent_storage_schema,
                "schema": schema,
                "volume": volume,
                "webURL": web_url,
                "projectId": project_id,
            }
        )
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        barcode = d.pop("barcode")

        checkout_record = CheckoutRecord.from_dict(d.pop("checkoutRecord"))

        contents = []
        _contents = d.pop("contents")
        for contents_item_data in _contents:
            contents_item = ContainerContent.from_dict(contents_item_data)

            contents.append(contents_item)

        created_at = isoparse(d.pop("createdAt"))

        creator = UserSummary.from_dict(d.pop("creator"))

        fields = Fields.from_dict(d.pop("fields"))

        modified_at = isoparse(d.pop("modifiedAt"))

        parent_storage_id = d.pop("parentStorageId")

        parent_storage_schema = SchemaSummary.from_dict(d.pop("parentStorageSchema"))

        schema = SchemaSummary.from_dict(d.pop("schema"))

        volume = Measurement.from_dict(d.pop("volume"))

        web_url = d.pop("webURL")

        archive_record: Union[Unset, ArchiveRecord] = UNSET
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = ArchiveRecord.from_dict(cast(Dict[str, Any], _archive_record))

        project_id = d.pop("projectId")

        container = cls(
            id=id,
            name=name,
            barcode=barcode,
            checkout_record=checkout_record,
            contents=contents,
            created_at=created_at,
            creator=creator,
            fields=fields,
            modified_at=modified_at,
            parent_storage_id=parent_storage_id,
            parent_storage_schema=parent_storage_schema,
            schema=schema,
            volume=volume,
            web_url=web_url,
            archive_record=archive_record,
            project_id=project_id,
        )

        return container
