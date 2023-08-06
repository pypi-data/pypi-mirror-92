from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.list_locations_sort import ListLocationsSort
from ...models.locations_paginated_list import LocationsPaginatedList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListLocationsSort] = ListLocationsSort.MODIFIEDAT,
    schema_id: Union[Unset, None, str] = UNSET,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    ancestor_storage_id: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    barcodes: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/locations".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_sort: Union[Unset, ListLocationsSort] = UNSET
    if not isinstance(sort, Unset) and sort is not None:
        json_sort = sort

    params: Dict[str, Any] = {}
    if page_size is not UNSET and page_size is not None:
        params["pageSize"] = page_size
    if next_token is not UNSET and next_token is not None:
        params["nextToken"] = next_token
    if sort is not UNSET and sort is not None:
        params["sort"] = json_sort
    if schema_id is not UNSET and schema_id is not None:
        params["schemaId"] = schema_id
    if modified_at is not UNSET and modified_at is not None:
        params["modifiedAt"] = modified_at
    if name is not UNSET and name is not None:
        params["name"] = name
    if name_includes is not UNSET and name_includes is not None:
        params["nameIncludes"] = name_includes
    if ancestor_storage_id is not UNSET and ancestor_storage_id is not None:
        params["ancestorStorageId"] = ancestor_storage_id
    if archive_reason is not UNSET and archive_reason is not None:
        params["archiveReason"] = archive_reason
    if ids is not UNSET and ids is not None:
        params["ids"] = ids
    if barcodes is not UNSET and barcodes is not None:
        params["barcodes"] = barcodes

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[LocationsPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = LocationsPaginatedList.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[LocationsPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListLocationsSort] = ListLocationsSort.MODIFIEDAT,
    schema_id: Union[Unset, None, str] = UNSET,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    ancestor_storage_id: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    barcodes: Union[Unset, None, str] = UNSET,
) -> Response[Union[LocationsPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        schema_id=schema_id,
        modified_at=modified_at,
        name=name,
        name_includes=name_includes,
        ancestor_storage_id=ancestor_storage_id,
        archive_reason=archive_reason,
        ids=ids,
        barcodes=barcodes,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListLocationsSort] = ListLocationsSort.MODIFIEDAT,
    schema_id: Union[Unset, None, str] = UNSET,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    ancestor_storage_id: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    barcodes: Union[Unset, None, str] = UNSET,
) -> Optional[Union[LocationsPaginatedList, BadRequestError]]:
    """  """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        schema_id=schema_id,
        modified_at=modified_at,
        name=name,
        name_includes=name_includes,
        ancestor_storage_id=ancestor_storage_id,
        archive_reason=archive_reason,
        ids=ids,
        barcodes=barcodes,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListLocationsSort] = ListLocationsSort.MODIFIEDAT,
    schema_id: Union[Unset, None, str] = UNSET,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    ancestor_storage_id: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    barcodes: Union[Unset, None, str] = UNSET,
) -> Response[Union[LocationsPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        schema_id=schema_id,
        modified_at=modified_at,
        name=name,
        name_includes=name_includes,
        ancestor_storage_id=ancestor_storage_id,
        archive_reason=archive_reason,
        ids=ids,
        barcodes=barcodes,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListLocationsSort] = ListLocationsSort.MODIFIEDAT,
    schema_id: Union[Unset, None, str] = UNSET,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    ancestor_storage_id: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    barcodes: Union[Unset, None, str] = UNSET,
) -> Optional[Union[LocationsPaginatedList, BadRequestError]]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            sort=sort,
            schema_id=schema_id,
            modified_at=modified_at,
            name=name,
            name_includes=name_includes,
            ancestor_storage_id=ancestor_storage_id,
            archive_reason=archive_reason,
            ids=ids,
            barcodes=barcodes,
        )
    ).parsed
