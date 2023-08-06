from typing import Any, Dict, Type, TypeVar, Union, cast

import attr

from ..models.automation_file_automation_file_config import AutomationFileAutomationFileConfig
from ..models.automation_file_file import AutomationFileFile
from ..types import UNSET, Unset

T = TypeVar("T", bound="AutomationInputGenerator")


@attr.s(auto_attribs=True)
class AutomationInputGenerator:
    """  """

    api_url: Union[Unset, str] = UNSET
    assay_run_id: Union[Unset, str] = UNSET
    automation_file_config: Union[Unset, AutomationFileAutomationFileConfig] = UNSET
    file: Union[Unset, AutomationFileFile] = UNSET
    id: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        api_url = self.api_url
        assay_run_id = self.assay_run_id
        automation_file_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.automation_file_config, Unset):
            automation_file_config = self.automation_file_config.to_dict()

        file: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_dict()

        id = self.id
        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if api_url is not UNSET:
            field_dict["apiURL"] = api_url
        if assay_run_id is not UNSET:
            field_dict["assayRunId"] = assay_run_id
        if automation_file_config is not UNSET:
            field_dict["automationFileConfig"] = automation_file_config
        if file is not UNSET:
            field_dict["file"] = file
        if id is not UNSET:
            field_dict["id"] = id
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        api_url = d.pop("apiURL", UNSET)

        assay_run_id = d.pop("assayRunId", UNSET)

        automation_file_config: Union[Unset, AutomationFileAutomationFileConfig] = UNSET
        _automation_file_config = d.pop("automationFileConfig", UNSET)
        if _automation_file_config is not None and not isinstance(_automation_file_config, Unset):
            automation_file_config = AutomationFileAutomationFileConfig.from_dict(
                cast(Dict[str, Any], _automation_file_config)
            )

        file: Union[Unset, AutomationFileFile] = UNSET
        _file = d.pop("file", UNSET)
        if _file is not None and not isinstance(_file, Unset):
            file = AutomationFileFile.from_dict(cast(Dict[str, Any], _file))

        id = d.pop("id", UNSET)

        status = d.pop("status", UNSET)

        automation_input_generator = cls(
            api_url=api_url,
            assay_run_id=assay_run_id,
            automation_file_config=automation_file_config,
            file=file,
            id=id,
            status=status,
        )

        return automation_input_generator
