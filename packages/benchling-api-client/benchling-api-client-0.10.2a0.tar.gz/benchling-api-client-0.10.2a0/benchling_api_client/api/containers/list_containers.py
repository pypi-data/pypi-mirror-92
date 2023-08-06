from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.containers_paginated_list import ContainersPaginatedList
from ...models.list_containers_checkout_status import ListContainersCheckoutStatus
from ...models.list_containers_sort import ListContainersSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListContainersSort] = ListContainersSort.MODIFIEDAT,
    schema_id: Union[Unset, None, str] = UNSET,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    ancestor_storage_id: Union[Unset, None, str] = UNSET,
    storage_contents_id: Union[Unset, None, str] = UNSET,
    storage_contents_ids: Union[Unset, None, List[str]] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    parent_storage_schema_id: Union[Unset, None, str] = UNSET,
    assay_run_id: Union[Unset, None, str] = UNSET,
    checkout_status: Union[Unset, None, ListContainersCheckoutStatus] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    barcodes: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/containers".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_sort: Union[Unset, ListContainersSort] = UNSET
    if not isinstance(sort, Unset) and sort is not None:
        json_sort = sort

    json_storage_contents_ids: Union[Unset, List[Any]] = UNSET
    if not isinstance(storage_contents_ids, Unset) and storage_contents_ids is not None:
        json_storage_contents_ids = storage_contents_ids

    json_checkout_status: Union[Unset, ListContainersCheckoutStatus] = UNSET
    if not isinstance(checkout_status, Unset) and checkout_status is not None:
        json_checkout_status = checkout_status

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
    if storage_contents_id is not UNSET and storage_contents_id is not None:
        params["storageContentsId"] = storage_contents_id
    if storage_contents_ids is not UNSET and storage_contents_ids is not None:
        params["storageContentsIds"] = json_storage_contents_ids
    if archive_reason is not UNSET and archive_reason is not None:
        params["archiveReason"] = archive_reason
    if parent_storage_schema_id is not UNSET and parent_storage_schema_id is not None:
        params["parentStorageSchemaId"] = parent_storage_schema_id
    if assay_run_id is not UNSET and assay_run_id is not None:
        params["assayRunId"] = assay_run_id
    if checkout_status is not UNSET and checkout_status is not None:
        params["checkoutStatus"] = json_checkout_status
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[ContainersPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = ContainersPaginatedList.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ContainersPaginatedList, BadRequestError]]:
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
    sort: Union[Unset, None, ListContainersSort] = ListContainersSort.MODIFIEDAT,
    schema_id: Union[Unset, None, str] = UNSET,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    ancestor_storage_id: Union[Unset, None, str] = UNSET,
    storage_contents_id: Union[Unset, None, str] = UNSET,
    storage_contents_ids: Union[Unset, None, List[str]] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    parent_storage_schema_id: Union[Unset, None, str] = UNSET,
    assay_run_id: Union[Unset, None, str] = UNSET,
    checkout_status: Union[Unset, None, ListContainersCheckoutStatus] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    barcodes: Union[Unset, None, str] = UNSET,
) -> Response[Union[ContainersPaginatedList, BadRequestError]]:
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
        storage_contents_id=storage_contents_id,
        storage_contents_ids=storage_contents_ids,
        archive_reason=archive_reason,
        parent_storage_schema_id=parent_storage_schema_id,
        assay_run_id=assay_run_id,
        checkout_status=checkout_status,
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
    sort: Union[Unset, None, ListContainersSort] = ListContainersSort.MODIFIEDAT,
    schema_id: Union[Unset, None, str] = UNSET,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    ancestor_storage_id: Union[Unset, None, str] = UNSET,
    storage_contents_id: Union[Unset, None, str] = UNSET,
    storage_contents_ids: Union[Unset, None, List[str]] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    parent_storage_schema_id: Union[Unset, None, str] = UNSET,
    assay_run_id: Union[Unset, None, str] = UNSET,
    checkout_status: Union[Unset, None, ListContainersCheckoutStatus] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    barcodes: Union[Unset, None, str] = UNSET,
) -> Optional[Union[ContainersPaginatedList, BadRequestError]]:
    """ List containers """

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
        storage_contents_id=storage_contents_id,
        storage_contents_ids=storage_contents_ids,
        archive_reason=archive_reason,
        parent_storage_schema_id=parent_storage_schema_id,
        assay_run_id=assay_run_id,
        checkout_status=checkout_status,
        ids=ids,
        barcodes=barcodes,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListContainersSort] = ListContainersSort.MODIFIEDAT,
    schema_id: Union[Unset, None, str] = UNSET,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    ancestor_storage_id: Union[Unset, None, str] = UNSET,
    storage_contents_id: Union[Unset, None, str] = UNSET,
    storage_contents_ids: Union[Unset, None, List[str]] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    parent_storage_schema_id: Union[Unset, None, str] = UNSET,
    assay_run_id: Union[Unset, None, str] = UNSET,
    checkout_status: Union[Unset, None, ListContainersCheckoutStatus] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    barcodes: Union[Unset, None, str] = UNSET,
) -> Response[Union[ContainersPaginatedList, BadRequestError]]:
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
        storage_contents_id=storage_contents_id,
        storage_contents_ids=storage_contents_ids,
        archive_reason=archive_reason,
        parent_storage_schema_id=parent_storage_schema_id,
        assay_run_id=assay_run_id,
        checkout_status=checkout_status,
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
    sort: Union[Unset, None, ListContainersSort] = ListContainersSort.MODIFIEDAT,
    schema_id: Union[Unset, None, str] = UNSET,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    ancestor_storage_id: Union[Unset, None, str] = UNSET,
    storage_contents_id: Union[Unset, None, str] = UNSET,
    storage_contents_ids: Union[Unset, None, List[str]] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    parent_storage_schema_id: Union[Unset, None, str] = UNSET,
    assay_run_id: Union[Unset, None, str] = UNSET,
    checkout_status: Union[Unset, None, ListContainersCheckoutStatus] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    barcodes: Union[Unset, None, str] = UNSET,
) -> Optional[Union[ContainersPaginatedList, BadRequestError]]:
    """ List containers """

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
            storage_contents_id=storage_contents_id,
            storage_contents_ids=storage_contents_ids,
            archive_reason=archive_reason,
            parent_storage_schema_id=parent_storage_schema_id,
            assay_run_id=assay_run_id,
            checkout_status=checkout_status,
            ids=ids,
            barcodes=barcodes,
        )
    ).parsed
