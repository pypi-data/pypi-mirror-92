from typing import Any, Dict, Optional, Type, TypeVar, Union, cast

import attr

from ..models.container_content_batch import ContainerContentBatch
from ..models.container_content_entity import ContainerContentEntity
from ..models.measurement import Measurement
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerContent")


@attr.s(auto_attribs=True)
class ContainerContent:
    """  """

    concentration: Measurement
    entity: Optional[ContainerContentEntity]
    batch: Union[Unset, None, ContainerContentBatch] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        concentration = self.concentration.to_dict()

        batch: Union[None, Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.batch, Unset):
            batch = self.batch.to_dict() if self.batch else None

        entity = self.entity.to_dict() if self.entity else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "concentration": concentration,
                "entity": entity,
            }
        )
        if batch is not UNSET:
            field_dict["batch"] = batch

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        concentration = Measurement.from_dict(d.pop("concentration"))

        batch = None
        _batch = d.pop("batch", UNSET)
        if _batch is not None and not isinstance(_batch, Unset):
            batch = ContainerContentBatch.from_dict(cast(Dict[str, Any], _batch))

        entity = ContainerContentEntity.from_dict(d.pop("entity"))

        container_content = cls(
            concentration=concentration,
            batch=batch,
            entity=entity,
        )

        return container_content
