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

from kelvin.sdk.lib.common.configs.internal.emulation_configs import StudioConfigs
from kelvin.sdk.lib.common.configs.internal.schema_manager_configs import SchemaManagerConfigs
from kelvin.sdk.lib.common.emulation.emulation_manager import emulation_start
from kelvin.sdk.lib.common.models.factories.docker_manager_factory import get_docker_manager
from kelvin.sdk.lib.common.models.factories.global_configurations_objects_factory import get_global_ksdk_configuration
from kelvin.sdk.lib.common.models.generic import KPath
from kelvin.sdk.lib.common.schema.schema_manager import get_latest_app_schema_version
from kelvin.sdk.lib.common.utils.general_utils import open_link_in_browser
from kelvin.sdk.lib.common.utils.logger_utils import logger


def studio_start(schema_file: Optional[str], input_file: str) -> bool:
    """
    Starts Kelvin Studio to modify the provided input.

    :param schema_file: the schema file used to power the Kelvin Studio's interface.
    :param input_file: the input file to modify based on the schema file..

    :return: a bool indicating whether the app start on the launchpad was successful.

    """
    try:
        # 1 - Load all the input files
        schema_file_path: KPath
        if not schema_file:
            get_latest_app_schema_version(overwrite_schema=True)
            schema_file_path = (
                KPath(SchemaManagerConfigs.schema_storage_path) / SchemaManagerConfigs.general_app_schema_file_name
            )
        else:
            schema_file_path = KPath(schema_file)
        schema_file_path = schema_file_path.expanduser().resolve().absolute()
        input_file_path = KPath(input_file).expanduser().resolve().absolute()

        if not schema_file_path.exists():
            raise FileNotFoundError(f"File not found {schema_file_path.absolute()}")
        if not input_file_path.exists():
            raise FileNotFoundError(f"File not found {input_file_path.absolute()}")

        logger.info(f'Starting Kelvin Studio with "{str(input_file)}"')

        # 2 - setup the binds, port mapping and arguments
        schema_file_bind: str = StudioConfigs.studio_schema_file_bind.format(
            schema_file_path=str(schema_file_path), schema_file_name=schema_file_path.name
        )
        config_file_bind: str = StudioConfigs.studio_input_file_bind.format(
            input_file_path=str(input_file_path), input_file_name=input_file_path.name
        )
        arguments = [schema_file_path.name, input_file_path.name]
        global_ksdk_configuration = get_global_ksdk_configuration()
        url_metadata = global_ksdk_configuration.get_metadata_for_url()
        all_launchpad_apps = url_metadata.sdk.launchpad
        studio_app_name = all_launchpad_apps["kelvin-studio"]

        # 1 - Jumpstart the application
        docker_manager = get_docker_manager()
        docker_manager.pull_docker_image_from_registry(docker_image_name=studio_app_name)

        successfully_started = emulation_start(
            app_name=studio_app_name,
            volumes=[schema_file_bind, config_file_bind],
            port_mapping=StudioConfigs.studio_port_mapping,
            arguments=arguments,
            is_external_app=True,
        )

        if successfully_started:
            studio_start_success: str = f"""

                    Kelvin Studio successfully started!
                    Use your browser of choice to access it on: \"{StudioConfigs.studio_default_url}\"

                    Opening Kelvin Studio...

                """
            logger.relevant(studio_start_success)
            import time

            time.sleep(3)
            return open_link_in_browser(StudioConfigs.studio_default_url)
        return successfully_started
    except Exception as exc:
        logger.error(f"Error starting Kelvin Studio: {str(exc)}")
        return False


def studio_stop() -> bool:
    """
    Stops a Kelvin Studio.

    :return: a bool indicating whether the Kelvin Studio was successfully stopped.

    """
    try:
        logger.info("Stopping Kelvin Studio")

        global_ksdk_configuration = get_global_ksdk_configuration()
        url_metadata = global_ksdk_configuration.get_metadata_for_url()
        all_launchpad_apps = url_metadata.sdk.launchpad
        studio_app_name = all_launchpad_apps["kelvin-studio"]

        docker_manager = get_docker_manager()
        docker_manager.stop_docker_containers_for_image(docker_image_name=studio_app_name)

        logger.relevant("Kelvin Studio successfully stopped")
        return True

    except Exception as exc:
        logger.error(f"Error stopping Kelvin Studio: {str(exc)}")
        return False
