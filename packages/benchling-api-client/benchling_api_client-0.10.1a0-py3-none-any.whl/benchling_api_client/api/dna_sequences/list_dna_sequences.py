from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.dna_sequences_paginated_list import DnaSequencesPaginatedList
from ...models.list_dna_sequences_sort import ListDNASequencesSort
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListDNASequencesSort] = ListDNASequencesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    bases: Union[Unset, None, str] = UNSET,
    folder_id: Union[Unset, None, str] = UNSET,
    mentioned_in: Union[Unset, None, List[str]] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    registry_id: Union[Unset, None, str] = UNSET,
    schema_id: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    mentions: Union[Unset, None, List[str]] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/dna-sequences".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_sort: Union[Unset, ListDNASequencesSort] = UNSET
    if not isinstance(sort, Unset) and sort is not None:
        json_sort = sort

    json_mentioned_in: Union[Unset, List[Any]] = UNSET
    if not isinstance(mentioned_in, Unset) and mentioned_in is not None:
        json_mentioned_in = mentioned_in

    json_mentions: Union[Unset, List[Any]] = UNSET
    if not isinstance(mentions, Unset) and mentions is not None:
        json_mentions = mentions

    params: Dict[str, Any] = {}
    if page_size is not UNSET and page_size is not None:
        params["pageSize"] = page_size
    if next_token is not UNSET and next_token is not None:
        params["nextToken"] = next_token
    if sort is not UNSET and sort is not None:
        params["sort"] = json_sort
    if modified_at is not UNSET and modified_at is not None:
        params["modifiedAt"] = modified_at
    if name is not UNSET and name is not None:
        params["name"] = name
    if bases is not UNSET and bases is not None:
        params["bases"] = bases
    if folder_id is not UNSET and folder_id is not None:
        params["folderId"] = folder_id
    if mentioned_in is not UNSET and mentioned_in is not None:
        params["mentionedIn"] = json_mentioned_in
    if project_id is not UNSET and project_id is not None:
        params["projectId"] = project_id
    if registry_id is not UNSET and registry_id is not None:
        params["registryId"] = registry_id
    if schema_id is not UNSET and schema_id is not None:
        params["schemaId"] = schema_id
    if archive_reason is not UNSET and archive_reason is not None:
        params["archiveReason"] = archive_reason
    if mentions is not UNSET and mentions is not None:
        params["mentions"] = json_mentions
    if ids is not UNSET and ids is not None:
        params["ids"] = ids
    if entity_registry_idsany_of is not UNSET and entity_registry_idsany_of is not None:
        params["entityRegistryIds.anyOf"] = entity_registry_idsany_of

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[DnaSequencesPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = DnaSequencesPaginatedList.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json())

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[DnaSequencesPaginatedList, BadRequestError]]:
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
    sort: Union[Unset, None, ListDNASequencesSort] = ListDNASequencesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    bases: Union[Unset, None, str] = UNSET,
    folder_id: Union[Unset, None, str] = UNSET,
    mentioned_in: Union[Unset, None, List[str]] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    registry_id: Union[Unset, None, str] = UNSET,
    schema_id: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    mentions: Union[Unset, None, List[str]] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, None, str] = UNSET,
) -> Response[Union[DnaSequencesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        bases=bases,
        folder_id=folder_id,
        mentioned_in=mentioned_in,
        project_id=project_id,
        registry_id=registry_id,
        schema_id=schema_id,
        archive_reason=archive_reason,
        mentions=mentions,
        ids=ids,
        entity_registry_idsany_of=entity_registry_idsany_of,
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
    sort: Union[Unset, None, ListDNASequencesSort] = ListDNASequencesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    bases: Union[Unset, None, str] = UNSET,
    folder_id: Union[Unset, None, str] = UNSET,
    mentioned_in: Union[Unset, None, List[str]] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    registry_id: Union[Unset, None, str] = UNSET,
    schema_id: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    mentions: Union[Unset, None, List[str]] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, None, str] = UNSET,
) -> Optional[Union[DnaSequencesPaginatedList, BadRequestError]]:
    """ List DNA sequences """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        bases=bases,
        folder_id=folder_id,
        mentioned_in=mentioned_in,
        project_id=project_id,
        registry_id=registry_id,
        schema_id=schema_id,
        archive_reason=archive_reason,
        mentions=mentions,
        ids=ids,
        entity_registry_idsany_of=entity_registry_idsany_of,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListDNASequencesSort] = ListDNASequencesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    bases: Union[Unset, None, str] = UNSET,
    folder_id: Union[Unset, None, str] = UNSET,
    mentioned_in: Union[Unset, None, List[str]] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    registry_id: Union[Unset, None, str] = UNSET,
    schema_id: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    mentions: Union[Unset, None, List[str]] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, None, str] = UNSET,
) -> Response[Union[DnaSequencesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        bases=bases,
        folder_id=folder_id,
        mentioned_in=mentioned_in,
        project_id=project_id,
        registry_id=registry_id,
        schema_id=schema_id,
        archive_reason=archive_reason,
        mentions=mentions,
        ids=ids,
        entity_registry_idsany_of=entity_registry_idsany_of,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Union[Unset, None, int] = 50,
    next_token: Union[Unset, None, str] = UNSET,
    sort: Union[Unset, None, ListDNASequencesSort] = ListDNASequencesSort.MODIFIEDATDESC,
    modified_at: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    bases: Union[Unset, None, str] = UNSET,
    folder_id: Union[Unset, None, str] = UNSET,
    mentioned_in: Union[Unset, None, List[str]] = UNSET,
    project_id: Union[Unset, None, str] = UNSET,
    registry_id: Union[Unset, None, str] = UNSET,
    schema_id: Union[Unset, None, str] = UNSET,
    archive_reason: Union[Unset, None, str] = UNSET,
    mentions: Union[Unset, None, List[str]] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    entity_registry_idsany_of: Union[Unset, None, str] = UNSET,
) -> Optional[Union[DnaSequencesPaginatedList, BadRequestError]]:
    """ List DNA sequences """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            sort=sort,
            modified_at=modified_at,
            name=name,
            bases=bases,
            folder_id=folder_id,
            mentioned_in=mentioned_in,
            project_id=project_id,
            registry_id=registry_id,
            schema_id=schema_id,
            archive_reason=archive_reason,
            mentions=mentions,
            ids=ids,
            entity_registry_idsany_of=entity_registry_idsany_of,
        )
    ).parsed
