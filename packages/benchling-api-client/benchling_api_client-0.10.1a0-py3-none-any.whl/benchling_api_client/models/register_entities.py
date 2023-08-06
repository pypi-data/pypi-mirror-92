from typing import Any, Dict, List, Type, TypeVar, cast

import attr

from ..models.register_entities_naming_strategy import RegisterEntitiesNamingStrategy

T = TypeVar("T", bound="RegisterEntities")


@attr.s(auto_attribs=True)
class RegisterEntities:
    """  """

    entity_ids: List[str]
    naming_strategy: RegisterEntitiesNamingStrategy

    def to_dict(self) -> Dict[str, Any]:
        entity_ids = self.entity_ids

        naming_strategy = self.naming_strategy.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "entityIds": entity_ids,
                "namingStrategy": naming_strategy,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_ids = cast(List[str], d.pop("entityIds"))

        naming_strategy = RegisterEntitiesNamingStrategy.from_dict(d.pop("namingStrategy"))

        register_entities = cls(
            entity_ids=entity_ids,
            naming_strategy=naming_strategy,
        )

        return register_entities
