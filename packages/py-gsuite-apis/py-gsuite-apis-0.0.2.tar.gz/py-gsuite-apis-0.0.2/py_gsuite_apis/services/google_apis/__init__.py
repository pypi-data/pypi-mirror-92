from abc import ABC, abstractmethod
from typing import Any, Union

import os
import logging

from googleapiclient.discovery import build as DiscoveryBuild
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from py_gsuite_apis.core.config import get_config
from py_gsuite_apis.services import fs_conn


settings = get_config()

logger = logging.getLogger("uvicorn")


class GoogleAuthCredentials(ABC):
    def __init__(self, *, credentials_filename: str = None, scope: str = None) -> None:
        self.creds = self.fetch_credentials(credentials_filename=credentials_filename, scope=scope)

    @abstractmethod
    def fetch_credentials(self, *, credentials_filename: str, scope: str) -> Any:
        raise NotImplementedError


class GoogleAuthCredentialsBase(GoogleAuthCredentials):
    def get_service_account_credentials_path(self, *, credentials_filename: str = None) -> str:
        if not credentials_filename:
            raise ValueError("Must provide a valid credentials filename.")

        service_credentials_path = None

        if settings.GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_FILEPATH:
            service_credentials_path = settings.GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_FILEPATH
            logger.info("Using credentials from " + service_credentials_path)

            if os.path.isfile(service_credentials_path):
                logger.info("Found file credentials in" + service_credentials_path)
                return service_credentials_path
            else:
                logger.warn(f"Service credentials path provided is invalid: {service_credentials_path}")

        if os.path.isfile(os.path.join(os.path.expanduser("~"), ".credentials", credentials_filename)):
            service_credentials_path = os.path.join(os.path.expanduser("~"), ".credentials", credentials_filename)
            logger.info("Using credentials from " + service_credentials_path)
            return service_credentials_path

        if os.path.isfile(os.path.join(".credentials", credentials_filename)):
            service_credentials_path = os.path.join(".credentials", credentials_filename)
            logger.info("Using credentials from " + service_credentials_path)
            return service_credentials_path

        raise Exception("UNABLE TO FIND CREDENTIALS FILE | Check the instructions in the setup_credentials.md file")


class GoogleWebAuthCredentials(GoogleAuthCredentialsBase):
    def fetch_credentials(self, *, credentials_filename: str = None, scope: str = None) -> Any:
        creds = fs_conn.fetch_google_oauth_token()

        SERVICE_ACCOUNT_CREDENTIALS_FILEPATH = self.get_service_account_credentials_path(
            credentials_filename=credentials_filename
        )

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    SERVICE_ACCOUNT_CREDENTIALS_FILEPATH,
                    # os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../../../{credentials_filename}"),
                    # f"../../{credentials_filename}",
                    scope,
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            fs_conn.save_google_oauth_credentials_to_pickle_file(creds)

        return creds


class GoogleServerAuthCredentials(GoogleAuthCredentialsBase):
    def fetch_credentials(self, *, credentials_filename: str = None, scope: str = None) -> Any:
        SERVICE_ACCOUNT_SCOPES = [
            "https://www.googleapis.com/auth/sqlservice.admin",
            settings.SLIDES.SCOPE,
            settings.SHEETS.SCOPE,
            settings.DRIVE.SCOPE,
        ]
        # SERVICE_ACCOUNT_FILEPATH = os.path.join(
        #     os.path.dirname(os.path.abspath(__file__)), f"../../../{credentials_filename}"
        # )
        SERVICE_ACCOUNT_CREDENTIALS_FILEPATH = self.get_service_account_credentials_path(
            credentials_filename=credentials_filename
        )

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_CREDENTIALS_FILEPATH, scopes=SERVICE_ACCOUNT_SCOPES
        )

        return credentials


class GoogleApiClient(object):
    def __init__(
        self,
        *,
        credentials: Union[GoogleWebAuthCredentials, GoogleServerAuthCredentials],
        build: str = None,
        version: str = None,
        scope: str = None,
    ) -> None:
        self.creds = credentials.creds
        self.scope = scope
        self.build = build
        self.version = version

        logger.info(f"AUTHORIZED SERVICE FOR: {build} - {version} WITH SCOPE={scope}")
        self.service = DiscoveryBuild(build, version, credentials=self.creds)


async def create_google_server_auth_services_credentials(
    credentials_filename: str = "google-service-account-credentials.json",
) -> GoogleServerAuthCredentials:
    return GoogleServerAuthCredentials(credentials_filename=credentials_filename)
