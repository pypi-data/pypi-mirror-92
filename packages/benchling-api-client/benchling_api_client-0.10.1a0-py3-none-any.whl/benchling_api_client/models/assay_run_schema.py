from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.assay_run_schema_archive_record import AssayRunSchemaArchiveRecord
from ..models.assay_run_schema_automation_input_file_configs_item import AssayRunSchemaAutomationInputFileConfigsItem
from ..models.assay_run_schema_automation_output_file_configs_item import AssayRunSchemaAutomationOutputFileConfigsItem
from ..models.assay_run_schema_organization import AssayRunSchemaOrganization
from ..models.assay_run_schema_type import AssayRunSchemaType
from ..models.schema_field import SchemaField
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssayRunSchema")


@attr.s(auto_attribs=True)
class AssayRunSchema:
    """  """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    archive_record: Union[Unset, None, AssayRunSchemaArchiveRecord] = UNSET
    field_definitions: Union[Unset, List[SchemaField]] = UNSET
    type: Union[Unset, AssayRunSchemaType] = UNSET
    system_name: Union[Unset, str] = UNSET
    derived_from: Union[Unset, None, str] = UNSET
    automation_input_file_configs: Union[Unset, List[AssayRunSchemaAutomationInputFileConfigsItem]] = UNSET
    automation_output_file_configs: Union[Unset, List[AssayRunSchemaAutomationOutputFileConfigsItem]] = UNSET
    organization: Union[Unset, AssayRunSchemaOrganization] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        archive_record: Union[None, Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        field_definitions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.field_definitions, Unset):
            field_definitions = []
            for field_definitions_item_data in self.field_definitions:
                field_definitions_item = field_definitions_item_data.to_dict()

                field_definitions.append(field_definitions_item)

        type: Union[Unset, AssayRunSchemaType] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type

        system_name = self.system_name
        derived_from = self.derived_from
        automation_input_file_configs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.automation_input_file_configs, Unset):
            automation_input_file_configs = []
            for automation_input_file_configs_item_data in self.automation_input_file_configs:
                automation_input_file_configs_item = automation_input_file_configs_item_data.to_dict()

                automation_input_file_configs.append(automation_input_file_configs_item)

        automation_output_file_configs: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.automation_output_file_configs, Unset):
            automation_output_file_configs = []
            for automation_output_file_configs_item_data in self.automation_output_file_configs:
                automation_output_file_configs_item = automation_output_file_configs_item_data.to_dict()

                automation_output_file_configs.append(automation_output_file_configs_item)

        organization: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.organization, Unset):
            organization = self.organization.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if field_definitions is not UNSET:
            field_dict["fieldDefinitions"] = field_definitions
        if type is not UNSET:
            field_dict["type"] = type
        if system_name is not UNSET:
            field_dict["systemName"] = system_name
        if derived_from is not UNSET:
            field_dict["derivedFrom"] = derived_from
        if automation_input_file_configs is not UNSET:
            field_dict["automationInputFileConfigs"] = automation_input_file_configs
        if automation_output_file_configs is not UNSET:
            field_dict["automationOutputFileConfigs"] = automation_output_file_configs
        if organization is not UNSET:
            field_dict["organization"] = organization

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = AssayRunSchemaArchiveRecord.from_dict(cast(Dict[str, Any], _archive_record))

        field_definitions = []
        _field_definitions = d.pop("fieldDefinitions", UNSET)
        for field_definitions_item_data in _field_definitions or []:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = AssayRunSchemaType(_type)

        system_name = d.pop("systemName", UNSET)

        derived_from = d.pop("derivedFrom", UNSET)

        automation_input_file_configs = []
        _automation_input_file_configs = d.pop("automationInputFileConfigs", UNSET)
        for automation_input_file_configs_item_data in _automation_input_file_configs or []:
            automation_input_file_configs_item = AssayRunSchemaAutomationInputFileConfigsItem.from_dict(
                automation_input_file_configs_item_data
            )

            automation_input_file_configs.append(automation_input_file_configs_item)

        automation_output_file_configs = []
        _automation_output_file_configs = d.pop("automationOutputFileConfigs", UNSET)
        for automation_output_file_configs_item_data in _automation_output_file_configs or []:
            automation_output_file_configs_item = AssayRunSchemaAutomationOutputFileConfigsItem.from_dict(
                automation_output_file_configs_item_data
            )

            automation_output_file_configs.append(automation_output_file_configs_item)

        organization: Union[Unset, AssayRunSchemaOrganization] = UNSET
        _organization = d.pop("organization", UNSET)
        if _organization is not None and not isinstance(_organization, Unset):
            organization = AssayRunSchemaOrganization.from_dict(cast(Dict[str, Any], _organization))

        assay_run_schema = cls(
            id=id,
            name=name,
            archive_record=archive_record,
            field_definitions=field_definitions,
            type=type,
            system_name=system_name,
            derived_from=derived_from,
            automation_input_file_configs=automation_input_file_configs,
            automation_output_file_configs=automation_output_file_configs,
            organization=organization,
        )

        return assay_run_schema
