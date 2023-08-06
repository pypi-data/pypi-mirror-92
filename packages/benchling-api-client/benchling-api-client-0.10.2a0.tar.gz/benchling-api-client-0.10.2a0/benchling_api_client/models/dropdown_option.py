from typing import Any, Dict, Type, TypeVar, Union, cast

import attr

from ..models.dropdown_option_archive_record import DropdownOptionArchiveRecord
from ..types import UNSET, Unset

T = TypeVar("T", bound="DropdownOption")


@attr.s(auto_attribs=True)
class DropdownOption:
    """  """

    name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    archive_record: Union[Unset, None, DropdownOptionArchiveRecord] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id = self.id
        archive_record: Union[None, Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if id is not UNSET:
            field_dict["id"] = id
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        id = d.pop("id", UNSET)

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = DropdownOptionArchiveRecord.from_dict(cast(Dict[str, Any], _archive_record))

        dropdown_option = cls(
            name=name,
            id=id,
            archive_record=archive_record,
        )

        return dropdown_option
