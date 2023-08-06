from typing import Any, Dict, KeysView, List, NamedTuple, Optional, Tuple, Union

import os
import time
import uuid
from collections import defaultdict
from copy import deepcopy

import requests
from requests.auth import HTTPBasicAuth

SEARCH_WAIT_SECONDS = 0.5


class Document(Dict[str, Any]):
    pass

    def as_dict(self) -> Dict[Any, Any]:
        return self


class Attribute(Dict[str, Any]):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        if "children" not in self:
            self["children"] = AttributeMap()

    @property
    def children(self):
        return self.get("children")

    def simple_value(self) -> Any:
        if "value" not in self:
            return None
        if "local_string" in self["value"]:
            return self["value"]["local_string"]["values"][
                self["value"]["local_string"]["official_locale"]
            ]
        else:
            return self["value"][list(self["value"].keys())[0]]

    def as_dict(self) -> Dict[Any, Any]:
        ret = {k: v for k, v in self.items()}
        ret["children"] = self["children"].as_dict()
        return ret


class AttributeMap:
    def __iter__(self):
        self.__keys: List[str] = list(self._attributes.keys())
        self.__index: int = 0

    def __next__(self):
        yield self._attributes[self.__keys[self.__index]]
        self.__index += 1

    def __len__(self):
        return len(self._attributes.items())

    def __getitem__(self, key: str) -> List[Attribute]:
        return self._attributes[key]

    def __repr__(self):
        return "AttributeMap({})".format(dict(**self._attributes).__repr__())

    def __init__(
        self,
        ids: List[str] = [],
        id_hash: Dict[str, Dict[Any, Any]] = {},
        parent_hash: Dict[str, List[str]] = {},
        flat_list: List[Dict[str, Any]] = [],
    ):
        # Internal only
        self._attributes: Dict[str, List[Attribute]] = defaultdict(list)

        if flat_list:
            # Lookup table
            id_hash = {v["value_id"]: v for v in flat_list}
            # Group all child ids by parent id if they have one
            parent_hash = defaultdict(list)
            for v in flat_list:
                if "parent_value_id" in v:
                    parent_hash[v["parent_value_id"]].append(v["value_id"])

            ids = [
                v["value_id"] for v in flat_list if not "parent_value_id" in v
            ]

        for id in ids:
            value: Dict[Any, Any] = id_hash[id]
            child_ids: List[str] = parent_hash[id]
            value["children"] = AttributeMap(
                ids=child_ids,
                id_hash=id_hash,
                parent_hash=parent_hash,
            )
            self._attributes[value["attribute_id"]].append(
                Attribute(**{k: v for k, v in value.items()})
            )

    def first(
        self, attribute: str, fail_on_not_present: bool = False
    ) -> Attribute:
        try:
            return self.get(attribute)[0]
        except IndexError:
            if fail_on_not_present is True:
                raise AttributeError(f'Attribute "{attribute}" not found')
            else:
                return Attribute()

    def get(self, attribute: str) -> List[Attribute]:
        try:
            return self.__getitem__(attribute)
        except KeyError:
            return []

    def as_dict(self) -> Dict[Any, Any]:
        ret = {}
        for attr, value_list in self._attributes.items():
            ret[attr] = [v.as_dict() for v in value_list]
        return ret


class Result(Dict[str, Any]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self["__raw"] = deepcopy(dict(**kwargs))
        self["documents"] = [Document(**d) for d in self["documents"]]
        self["values"] = AttributeMap(flat_list=self["values"])

    def as_dict(self):
        ret = {k: v for k, v in self.items()}
        ret["documents"] = [d.as_dict() for d in self["documents"]]
        ret["values"] = self["values"].as_dict()
        return ret


class SearchPage(Dict[str, Any]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self["results"] = [Result(**r) for r in self["results"]]

    def as_dict(self):
        ret = {k: v for k, v in self.items()}
        ret["results"] = [r.as_dict() for r in self["results"]]
        return ret


class APIClient:

    PATHS: Dict[str, str] = {
        "REQUEST_TOKEN_REFRESH": "api/user-management/v1/oauth2/token",
        "LIST_SOURCES": "api/unisearch/v1/sources/",
        "GET_SOURCE": "api/unisearch/v1/sources/{id}",
        "SEARCH": "api/unisearch/v1/searches/{uuid}",
        "SEARCH_RESULTS": "api/unisearch/v1/searches/{uuid}/results",
        "SEARCH_RESULT_DETAILS": "api/unisearch/v1/searches/{uuid}/results/{result_id}",
        "SEARCH_DOCUMENT": "api/unisearch/v1/searches/{uuid}/results/{result_id}/documents/{document_id}",
    }

    def __init__(
        self,
        user_id: str = "",
        secret_id: str = "",
        secret_key: str = "",
        api_base: str = "",
    ) -> None:
        self._user_id = user_id or os.getenv(
            "ARACHNYS_PLATFORM_USER_ID", default=""
        )
        self._secret_id = secret_id or os.getenv(
            "ARACHNYS_PLATFORM_SECRET_ID", default=""
        )
        self._secret_key = secret_key or os.getenv(
            "ARACHNYS_PLATFORM_SECRET_KEY", default=""
        )
        self._access_token: Optional[str] = None
        self._api_base = api_base or os.getenv(
            "ARACHNYS_PLATFORM_API_BASE",
            default="https://platform.arachnys.com/",
        )

    def refresh_token(self) -> Optional[str]:
        resp: requests.Response = requests.post(
            self._api_base + self.PATHS["REQUEST_TOKEN_REFRESH"],
            json={
                "grant_type": "client_credentials",
            },
            auth=HTTPBasicAuth(
                f"{self._user_id}:{self._secret_id}", self._secret_key
            ),
        )
        resp.raise_for_status()
        self._access_token = resp.json()["access_token"]
        return self._access_token

    def _make_authenticated_call(
        self,
        method: str,
        path: str,
        params: Optional[Dict[Any, Any]] = None,
        json: Optional[Dict[Any, Any]] = None,
        retry_on_token_expired: bool = True,
        max_retry_time: int = 30,
    ) -> requests.Response:
        elapsed_retry_time = 0
        if self._access_token is None:
            self.refresh_token()
        while elapsed_retry_time < max_retry_time:
            resp: requests.Response = requests.request(
                method=method,
                url=self._api_base + path,
                headers={"authorization": f"Bearer {self._access_token}"},
                params=params,
                json=json,
            )
            if (
                resp.status_code in [403, 401]
                and retry_on_token_expired is True
            ):
                self._access_token = None
                return self._make_authenticated_call(
                    method,
                    path,
                    params,
                    json,
                    retry_on_token_expired=False,
                    max_retry_time=max_retry_time,
                )
            elif resp.status_code == 503:
                try:
                    retry_after: int = int(resp.headers["retry-after"])
                except:  # Something's wrong if header missing
                    resp.raise_for_status()
                time.sleep(retry_after)
                elapsed_retry_time += retry_after
            else:
                return resp
        return resp

    def sources(
        self,
        id: Optional[str] = None,
        query: Optional[str] = None,
        category_ids: List[str] = [],
        jurisdictions: List[str] = [],
        return_attribute_ids: List[str] = [],
    ) -> Any:
        if id is not None:
            return self._make_authenticated_call(
                method="GET",
                path=self.PATHS["GET_SOURCE"].format(id=id),
            ).json()
        else:
            params: Dict[str, Any] = {}
            if query:
                params["query"] = query
            if category_ids:
                params["category_ids"] = category_ids
            if jurisdictions:
                params["jurisdictions"] = jurisdictions
            if return_attribute_ids:
                params["return_attribute_ids"] = return_attribute_ids
            return self._make_authenticated_call(
                method="GET",
                path=self.PATHS["LIST_SOURCES"],
                params=params,
            ).json()

    def _put_search(
        self,
        source_ids: List[str],
        filter: List[
            Dict[str, Any]
        ],  # TODO - should be more strongly typed ideally
        limit: int,
        rate_limit_backoff: bool = False,  # Fail if rate limited by default, otherwise gracefully obey
    ) -> uuid.UUID:
        search_id: uuid.UUID = uuid.uuid4()
        resp: requests.Response = self._make_authenticated_call(
            method="PUT",
            path=self.PATHS["SEARCH"].format(uuid=str(search_id)),
            json={
                "source_ids": source_ids,
                "filter": filter,
                "limit": limit,
            },
        )
        if not rate_limit_backoff:
            resp.raise_for_status()
        else:
            raise NotImplementedError()
        return search_id

    def _get_search_page(
        self,
        search_id: uuid.UUID,
        cursor: Optional[str] = None,
        elapsed_retry_time: int = 0,
        max_retry_time: int = 30,  # Set to 0 to fail on first `retry-after` message
    ) -> SearchPage:
        params = {}
        if cursor:
            params["cursor"] = cursor
        resp = self._make_authenticated_call(
            method="GET",
            path=self.PATHS["SEARCH_RESULTS"].format(uuid=str(search_id)),
            params=params,
            max_retry_time=max_retry_time,
        )
        resp.raise_for_status()
        return SearchPage(**resp.json())

    def search(
        self,
        source_ids: List[str],
        filter: List[Dict[str, Any]],
        limit: int = 10,
        max_retry_time: int = 30,
    ) -> SearchPage:
        search_id: uuid.UUID = self._put_search(
            source_ids=source_ids,
            filter=filter,
            limit=limit,
        )
        time.sleep(SEARCH_WAIT_SECONDS)
        return self._get_search_page(
            search_id=search_id,
            max_retry_time=max_retry_time,
        )

    def paginate_search(
        self,
        cursor: str,
        search_id: Union[str, uuid.UUID],
        max_retry_time: int = 30,
    ) -> SearchPage:
        if isinstance(search_id, str):
            search_id = uuid.UUID(search_id)
        return self._get_search_page(
            search_id=search_id,
            cursor=cursor,
            max_retry_time=max_retry_time,
        )

    def get_result_details(
        self,
        search_id: Union[uuid.UUID, str],
        result_id: str,
    ) -> Result:
        if isinstance(search_id, str):
            search_id = uuid.UUID(search_id)
        resp = self._make_authenticated_call(
            "GET",
            path=self.PATHS["SEARCH_RESULT_DETAILS"].format(
                uuid=str(search_id),
                result_id=result_id,
            ),
        )
        resp.raise_for_status()
        return Result(**resp.json())

    def get_document(
        self,
        search_id: Union[uuid.UUID, str],
        result_id: str,
        document_id: str,
        elapsed_retry_time: int = 0,
        max_retry_time: int = 30,  # Set to 0 to fail on first `retry-after` message
    ) -> bytes:
        """We don't know what format this is in"""
        if isinstance(search_id, str):
            search_id = uuid.UUID(search_id)
        resp = self._make_authenticated_call(
            "GET",
            path=self.PATHS["SEARCH_DOCUMENT"].format(
                uuid=search_id,
                result_id=result_id,
                document_id=document_id,
            ),
            max_retry_time=max_retry_time,
        )
        resp.raise_for_status()
        download_url = resp.json()["download_url"]
        s3_resp = requests.get(download_url)
        s3_resp.raise_for_status()
        return s3_resp.content
