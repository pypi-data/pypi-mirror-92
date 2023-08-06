from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.box_schema_container_schema import BoxSchemaContainerSchema
from ..models.schema_field import SchemaField
from ..types import UNSET, Unset

T = TypeVar("T", bound="PlateSchema")


@attr.s(auto_attribs=True)
class PlateSchema:
    """  """

    plate_type: Union[Unset, str] = UNSET
    height: Union[Unset, float] = UNSET
    width: Union[Unset, float] = UNSET
    container_schema: Union[Unset, BoxSchemaContainerSchema] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    field_definitions: Union[Unset, List[SchemaField]] = UNSET
    type: Union[Unset, str] = UNSET
    prefix: Union[Unset, str] = UNSET
    registry_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        plate_type = self.plate_type
        height = self.height
        width = self.width
        container_schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.container_schema, Unset):
            container_schema = self.container_schema.to_dict()

        id = self.id
        name = self.name
        field_definitions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.field_definitions, Unset):
            field_definitions = []
            for field_definitions_item_data in self.field_definitions:
                field_definitions_item = field_definitions_item_data.to_dict()

                field_definitions.append(field_definitions_item)

        type = self.type
        prefix = self.prefix
        registry_id = self.registry_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if plate_type is not UNSET:
            field_dict["plateType"] = plate_type
        if height is not UNSET:
            field_dict["height"] = height
        if width is not UNSET:
            field_dict["width"] = width
        if container_schema is not UNSET:
            field_dict["containerSchema"] = container_schema
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if field_definitions is not UNSET:
            field_dict["fieldDefinitions"] = field_definitions
        if type is not UNSET:
            field_dict["type"] = type
        if prefix is not UNSET:
            field_dict["prefix"] = prefix
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        plate_type = d.pop("plateType", UNSET)

        height = d.pop("height", UNSET)

        width = d.pop("width", UNSET)

        container_schema: Union[Unset, BoxSchemaContainerSchema] = UNSET
        _container_schema = d.pop("containerSchema", UNSET)
        if _container_schema is not None and not isinstance(_container_schema, Unset):
            container_schema = BoxSchemaContainerSchema.from_dict(cast(Dict[str, Any], _container_schema))

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        field_definitions = []
        _field_definitions = d.pop("fieldDefinitions", UNSET)
        for field_definitions_item_data in _field_definitions or []:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        type = d.pop("type", UNSET)

        prefix = d.pop("prefix", UNSET)

        registry_id = d.pop("registryId", UNSET)

        plate_schema = cls(
            plate_type=plate_type,
            height=height,
            width=width,
            container_schema=container_schema,
            id=id,
            name=name,
            field_definitions=field_definitions,
            type=type,
            prefix=prefix,
            registry_id=registry_id,
        )

        return plate_schema
