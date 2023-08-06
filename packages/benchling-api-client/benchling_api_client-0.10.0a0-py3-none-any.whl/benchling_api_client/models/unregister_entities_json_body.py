from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="UnregisterEntitiesJsonBody")


@attr.s(auto_attribs=True)
class UnregisterEntitiesJsonBody:
    """  """

    entity_ids: List[str]
    folder_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entity_ids = self.entity_ids

        folder_id = self.folder_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entityIds": entity_ids,
                "folderId": folder_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_ids = cast(List[str], d.pop("entityIds"))

        folder_id = d.pop("folderId")

        unregister_entities_json_body = cls(
            entity_ids=entity_ids,
            folder_id=folder_id,
        )

        unregister_entities_json_body.additional_properties = d
        return unregister_entities_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
