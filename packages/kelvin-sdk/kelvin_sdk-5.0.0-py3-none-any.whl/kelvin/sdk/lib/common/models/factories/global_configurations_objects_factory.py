"""
Copyright 2021 Kelvin Inc.

Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

http://www.kelvininc.com/developer-sdk-license

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
"""
from typing import Optional

from kelvin.sdk.cli.version import version
from kelvin.sdk.client import Client
from kelvin.sdk.lib.common.configs.internal.auth_manager_configs import AuthManagerConfigs
from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs, KSDKHelpMessages
from kelvin.sdk.lib.common.models.generic import KPath
from kelvin.sdk.lib.common.models.ksdk_docker import KSDKDockerAuthentication
from kelvin.sdk.lib.common.models.ksdk_global_configuration import KelvinSDKConfiguration, KelvinSDKGlobalConfiguration


def get_global_ksdk_configuration(
    ksdk_config_file_path: Optional[KPath] = None, kelvin_sdk_client_config_file_path: Optional[KPath] = None
) -> KelvinSDKGlobalConfiguration:
    """
    Attempt to retrieve the KelvinSDKGlobalConfiguration from specified file path.

    :param ksdk_config_file_path: the path to the KSDK configuration file.
    :param kelvin_sdk_client_config_file_path: the path to the Kelvin API Client configuration file.

    :return: a KelvinSDKGlobalConfiguration object corresponding to the current configuration.

    """
    try:
        if not ksdk_config_file_path:
            default_path = GeneralConfigs.default_ksdk_configuration_file
            ksdk_config_file_path = KPath(default_path).expanduser().resolve()

        if not kelvin_sdk_client_config_file_path:
            default_path = GeneralConfigs.default_kelvin_sdk_client_configuration_file
            kelvin_sdk_client_config_file_path = KPath(default_path).expanduser().resolve()

        # 2 - Load the  existing configuration
        loaded_ksdk_configuration_dict = ksdk_config_file_path.read_yaml(verbose=False) if ksdk_config_file_path else {}
        loaded_ksdk_configuration_dict.update({"ksdk_current_version": version})
        ksdk_config = KelvinSDKConfiguration(**loaded_ksdk_configuration_dict)

        return KelvinSDKGlobalConfiguration(
            kelvin_sdk_client_config_file_path=kelvin_sdk_client_config_file_path,
            ksdk_config_file_path=ksdk_config_file_path,
            kelvin_sdk=ksdk_config,
        )
    except Exception:
        ksdk_configuration: KelvinSDKGlobalConfiguration = KelvinSDKGlobalConfiguration(
            kelvin_sdk_client_config_file_path=kelvin_sdk_client_config_file_path,
            ksdk_config_file_path=ksdk_config_file_path,
            kelvin_sdk=KelvinSDKConfiguration(
                current_url="",
                current_user="",
                ksdk_current_version=version,
                ksdk_minimum_version=version,
                ksdk_latest_version=version,
            ),
        )
        return ksdk_configuration.commit_ksdk_configuration()


def get_docker_credentials_for_current_url() -> KSDKDockerAuthentication:
    """
    Returns the current credentials for the specified url.

    :return: a dictionary containing the Kelvin API Client credentials for the specified url.

    """
    try:
        ksdk_configuration = get_global_ksdk_configuration()

        current_url = ksdk_configuration.kelvin_sdk.current_url
        current_user = ksdk_configuration.kelvin_sdk.current_user
        current_site_metadata = ksdk_configuration.get_metadata_for_url()

        if current_site_metadata:
            client = Client.from_file(
                filename=ksdk_configuration.kelvin_sdk_client_config_file_path,
                username=current_user,
                realm_name=current_site_metadata.authentication.realm,
                site=current_url,
                url=current_url,
            )
            return KSDKDockerAuthentication(
                **{
                    "registry_url": current_site_metadata.docker.url,
                    "registry_port": current_site_metadata.docker.port,
                    "username": current_user,
                    "password": client.password,
                }
            )
        raise ValueError
    except Exception:
        raise ConnectionError(AuthManagerConfigs.invalid_session_message)


def get_documentation_link_for_current_url() -> Optional[str]:
    """
    Retrieve, if existent, the complete url to the documentation page.

    :return: a string containing a link to the documentation page.

    """
    try:
        global_ksdk_configuration = get_global_ksdk_configuration()
        if global_ksdk_configuration:
            current_metadata = global_ksdk_configuration.get_metadata_for_url()
            if current_metadata and current_metadata.documentation:
                return current_metadata.documentation.url
    except Exception:
        pass
    return None


def get_current_session_platform() -> Optional[str]:
    """
    Retrieve, if existent, the current session's url.

    :return: a string containing the current session's url.

    """
    try:
        ksdk_configuration = get_global_ksdk_configuration()
        current_url = ksdk_configuration.kelvin_sdk.current_url
        if current_url:
            return current_url
    except Exception:
        pass
    return KSDKHelpMessages.current_session_login
