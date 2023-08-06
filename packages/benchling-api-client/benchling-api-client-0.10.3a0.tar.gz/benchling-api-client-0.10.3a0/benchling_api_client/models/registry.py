from typing import Any, Dict, Type, TypeVar, Union, cast

import attr

from ..models.organization import Organization
from ..types import UNSET, Unset

T = TypeVar("T", bound="Registry")


@attr.s(auto_attribs=True)
class Registry:
    """  """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    owner: Union[Unset, Organization] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        owner: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.owner, Unset):
            owner = self.owner.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if owner is not UNSET:
            field_dict["owner"] = owner

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        owner: Union[Unset, Organization] = UNSET
        _owner = d.pop("owner", UNSET)
        if _owner is not None and not isinstance(_owner, Unset):
            owner = Organization.from_dict(cast(Dict[str, Any], _owner))

        registry = cls(
            id=id,
            name=name,
            owner=owner,
        )

        return registry
