from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.boxes_paginated_list import BoxesPaginatedList
from ...models.list_boxes_sort import ListBoxesSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListBoxesSort] = ListBoxesSort.MODIFIEDATDESC,
    schema_id: Union[Unset, None, str] = UNSET,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    empty_positions: Union[Unset, None, int] = UNSET,
    empty_positionsgte: Union[Unset, None, int] = UNSET,
    empty_positionsgt: Union[Unset, None, int] = UNSET,
    empty_positionslte: Union[Unset, None, int] = UNSET,
    empty_positionslt: Union[Unset, None, int] = UNSET,
    empty_containers: Union[Unset, None, int] = UNSET,
    empty_containersgte: Union[Unset, None, int] = UNSET,
    empty_containersgt: Union[Unset, None, int] = UNSET,
    empty_containerslte: Union[Unset, None, int] = UNSET,
    empty_containerslt: Union[Unset, None, int] = UNSET,
    ancestor_storage_id: Union[Unset, None, str] = UNSET,
    storage_contents_id: Union[Unset, None, str] = UNSET,
    storage_contents_ids: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    barcodes: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/boxes".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_sort: Union[Unset, ListBoxesSort] = UNSET
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
    if empty_positions is not UNSET and empty_positions is not None:
        params["emptyPositions"] = empty_positions
    if empty_positionsgte is not UNSET and empty_positionsgte is not None:
        params["emptyPositions.gte"] = empty_positionsgte
    if empty_positionsgt is not UNSET and empty_positionsgt is not None:
        params["emptyPositions.gt"] = empty_positionsgt
    if empty_positionslte is not UNSET and empty_positionslte is not None:
        params["emptyPositions.lte"] = empty_positionslte
    if empty_positionslt is not UNSET and empty_positionslt is not None:
        params["emptyPositions.lt"] = empty_positionslt
    if empty_containers is not UNSET and empty_containers is not None:
        params["emptyContainers"] = empty_containers
    if empty_containersgte is not UNSET and empty_containersgte is not None:
        params["emptyContainers.gte"] = empty_containersgte
    if empty_containersgt is not UNSET and empty_containersgt is not None:
        params["emptyContainers.gt"] = empty_containersgt
    if empty_containerslte is not UNSET and empty_containerslte is not None:
        params["emptyContainers.lte"] = empty_containerslte
    if empty_containerslt is not UNSET and empty_containerslt is not None:
        params["emptyContainers.lt"] = empty_containerslt
    if ancestor_storage_id is not UNSET and ancestor_storage_id is not None:
        params["ancestorStorageId"] = ancestor_storage_id
    if storage_contents_id is not UNSET and storage_contents_id is not None:
        params["storageContentsId"] = storage_contents_id
    if storage_contents_ids is not UNSET and storage_contents_ids is not None:
        params["storageContentsIds"] = storage_contents_ids
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[BoxesPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = BoxesPaginatedList.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[BoxesPaginatedList, BadRequestError]]:
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
    sort: Union[Unset, None, ListBoxesSort] = ListBoxesSort.MODIFIEDATDESC,
    schema_id: Union[Unset, None, str] = UNSET,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    empty_positions: Union[Unset, None, int] = UNSET,
    empty_positionsgte: Union[Unset, None, int] = UNSET,
    empty_positionsgt: Union[Unset, None, int] = UNSET,
    empty_positionslte: Union[Unset, None, int] = UNSET,
    empty_positionslt: Union[Unset, None, int] = UNSET,
    empty_containers: Union[Unset, None, int] = UNSET,
    empty_containersgte: Union[Unset, None, int] = UNSET,
    empty_containersgt: Union[Unset, None, int] = UNSET,
    empty_containerslte: Union[Unset, None, int] = UNSET,
    empty_containerslt: Union[Unset, None, int] = UNSET,
    ancestor_storage_id: Union[Unset, None, str] = UNSET,
    storage_contents_id: Union[Unset, None, str] = UNSET,
    storage_contents_ids: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    barcodes: Union[Unset, None, str] = UNSET,
) -> Response[Union[BoxesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        schema_id=schema_id,
        modified_at=modified_at,
        name=name,
        name_includes=name_includes,
        empty_positions=empty_positions,
        empty_positionsgte=empty_positionsgte,
        empty_positionsgt=empty_positionsgt,
        empty_positionslte=empty_positionslte,
        empty_positionslt=empty_positionslt,
        empty_containers=empty_containers,
        empty_containersgte=empty_containersgte,
        empty_containersgt=empty_containersgt,
        empty_containerslte=empty_containerslte,
        empty_containerslt=empty_containerslt,
        ancestor_storage_id=ancestor_storage_id,
        storage_contents_id=storage_contents_id,
        storage_contents_ids=storage_contents_ids,
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
    sort: Union[Unset, None, ListBoxesSort] = ListBoxesSort.MODIFIEDATDESC,
    schema_id: Union[Unset, None, str] = UNSET,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    empty_positions: Union[Unset, None, int] = UNSET,
    empty_positionsgte: Union[Unset, None, int] = UNSET,
    empty_positionsgt: Union[Unset, None, int] = UNSET,
    empty_positionslte: Union[Unset, None, int] = UNSET,
    empty_positionslt: Union[Unset, None, int] = UNSET,
    empty_containers: Union[Unset, None, int] = UNSET,
    empty_containersgte: Union[Unset, None, int] = UNSET,
    empty_containersgt: Union[Unset, None, int] = UNSET,
    empty_containerslte: Union[Unset, None, int] = UNSET,
    empty_containerslt: Union[Unset, None, int] = UNSET,
    ancestor_storage_id: Union[Unset, None, str] = UNSET,
    storage_contents_id: Union[Unset, None, str] = UNSET,
    storage_contents_ids: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    barcodes: Union[Unset, None, str] = UNSET,
) -> Optional[Union[BoxesPaginatedList, BadRequestError]]:
    """ List boxes """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        schema_id=schema_id,
        modified_at=modified_at,
        name=name,
        name_includes=name_includes,
        empty_positions=empty_positions,
        empty_positionsgte=empty_positionsgte,
        empty_positionsgt=empty_positionsgt,
        empty_positionslte=empty_positionslte,
        empty_positionslt=empty_positionslt,
        empty_containers=empty_containers,
        empty_containersgte=empty_containersgte,
        empty_containersgt=empty_containersgt,
        empty_containerslte=empty_containerslte,
        empty_containerslt=empty_containerslt,
        ancestor_storage_id=ancestor_storage_id,
        storage_contents_id=storage_contents_id,
        storage_contents_ids=storage_contents_ids,
        archive_reason=archive_reason,
        ids=ids,
        barcodes=barcodes,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListBoxesSort] = ListBoxesSort.MODIFIEDATDESC,
    schema_id: Union[Unset, None, str] = UNSET,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    empty_positions: Union[Unset, None, int] = UNSET,
    empty_positionsgte: Union[Unset, None, int] = UNSET,
    empty_positionsgt: Union[Unset, None, int] = UNSET,
    empty_positionslte: Union[Unset, None, int] = UNSET,
    empty_positionslt: Union[Unset, None, int] = UNSET,
    empty_containers: Union[Unset, None, int] = UNSET,
    empty_containersgte: Union[Unset, None, int] = UNSET,
    empty_containersgt: Union[Unset, None, int] = UNSET,
    empty_containerslte: Union[Unset, None, int] = UNSET,
    empty_containerslt: Union[Unset, None, int] = UNSET,
    ancestor_storage_id: Union[Unset, None, str] = UNSET,
    storage_contents_id: Union[Unset, None, str] = UNSET,
    storage_contents_ids: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    barcodes: Union[Unset, None, str] = UNSET,
) -> Response[Union[BoxesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        schema_id=schema_id,
        modified_at=modified_at,
        name=name,
        name_includes=name_includes,
        empty_positions=empty_positions,
        empty_positionsgte=empty_positionsgte,
        empty_positionsgt=empty_positionsgt,
        empty_positionslte=empty_positionslte,
        empty_positionslt=empty_positionslt,
        empty_containers=empty_containers,
        empty_containersgte=empty_containersgte,
        empty_containersgt=empty_containersgt,
        empty_containerslte=empty_containerslte,
        empty_containerslt=empty_containerslt,
        ancestor_storage_id=ancestor_storage_id,
        storage_contents_id=storage_contents_id,
        storage_contents_ids=storage_contents_ids,
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
    sort: Union[Unset, None, ListBoxesSort] = ListBoxesSort.MODIFIEDATDESC,
    schema_id: Union[Unset, None, str] = UNSET,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    name_includes: Union[Unset, None, str] = UNSET,
    empty_positions: Union[Unset, None, int] = UNSET,
    empty_positionsgte: Union[Unset, None, int] = UNSET,
    empty_positionsgt: Union[Unset, None, int] = UNSET,
    empty_positionslte: Union[Unset, None, int] = UNSET,
    empty_positionslt: Union[Unset, None, int] = UNSET,
    empty_containers: Union[Unset, None, int] = UNSET,
    empty_containersgte: Union[Unset, None, int] = UNSET,
    empty_containersgt: Union[Unset, None, int] = UNSET,
    empty_containerslte: Union[Unset, None, int] = UNSET,
    empty_containerslt: Union[Unset, None, int] = UNSET,
    ancestor_storage_id: Union[Unset, None, str] = UNSET,
    storage_contents_id: Union[Unset, None, str] = UNSET,
    storage_contents_ids: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    barcodes: Union[Unset, None, str] = UNSET,
) -> Optional[Union[BoxesPaginatedList, BadRequestError]]:
    """ List boxes """

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
            empty_positions=empty_positions,
            empty_positionsgte=empty_positionsgte,
            empty_positionsgt=empty_positionsgt,
            empty_positionslte=empty_positionslte,
            empty_positionslt=empty_positionslt,
            empty_containers=empty_containers,
            empty_containersgte=empty_containersgte,
            empty_containersgt=empty_containersgt,
            empty_containerslte=empty_containerslte,
            empty_containerslt=empty_containerslt,
            ancestor_storage_id=ancestor_storage_id,
            storage_contents_id=storage_contents_id,
            storage_contents_ids=storage_contents_ids,
            archive_reason=archive_reason,
            ids=ids,
            barcodes=barcodes,
        )
    ).parsed
