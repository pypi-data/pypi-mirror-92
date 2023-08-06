from typing import Any, Dict, Type, TypeVar, Union, cast

import attr

from ..models.sample_group_samples import SampleGroupSamples
from ..types import UNSET, Unset

T = TypeVar("T", bound="SampleGroup")


@attr.s(auto_attribs=True)
class SampleGroup:
    """ Represents a sample group that is an input to a request. A sample group is a set of samples upon which work in the request should be done. """

    id: Union[Unset, str] = UNSET
    samples: Union[Unset, SampleGroupSamples] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        samples: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.samples, Unset):
            samples = self.samples.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if samples is not UNSET:
            field_dict["samples"] = samples

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        samples: Union[Unset, SampleGroupSamples] = UNSET
        _samples = d.pop("samples", UNSET)
        if _samples is not None and not isinstance(_samples, Unset):
            samples = SampleGroupSamples.from_dict(cast(Dict[str, Any], _samples))

        sample_group = cls(
            id=id,
            samples=samples,
        )

        return sample_group
