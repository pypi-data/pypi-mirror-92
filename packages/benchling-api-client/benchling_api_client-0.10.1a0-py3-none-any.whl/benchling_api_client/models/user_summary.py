from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserSummary")


@attr.s(auto_attribs=True)
class UserSummary:
    """  """

    name: Union[Unset, str] = UNSET
    handle: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        handle = self.handle
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if handle is not UNSET:
            field_dict["handle"] = handle
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        handle = d.pop("handle", UNSET)

        id = d.pop("id", UNSET)

        user_summary = cls(
            name=name,
            handle=handle,
            id=id,
        )

        return user_summary
