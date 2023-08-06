import logging

import requests

from slate_utils.common.exceptions import ConsolidatedRecordsError
from slate_utils.session import SlateSession

logging.getLogger(__name__).addHandler(logging.NullHandler())


class ConsolidateRecords:
    scopes = [
        "person",
        "dataset",
        "school",
        "relation",
        "relation_related",
        "school_key",
        "job_key",
    ]

    def __init__(self, session: SlateSession):
        self.hostname = session.headers.get("origin")
        self.session = session

    def refresh_one(self, scope: str) -> requests.Response:
        """Refresh a single scope

        Parameters
        scope : str
           The scope to refresh (person, school_key, relation, etc.)
        """
        url = f"{self.hostname}/manage/database/dedupe?cmd=refresh&scope={scope}"
        response = self.session.get(url)
        response.raise_for_status()
        logging.info(f"Refreshed scope: {scope} {response.text}")
        try:
            assert response.text == "OK"
        except AssertionError:
            raise ConsolidatedRecordsError(f"{scope}: {response.text}")
        return response

    def refresh_all(self):
        for scope in self.scopes:
            self.refresh_one(scope)
