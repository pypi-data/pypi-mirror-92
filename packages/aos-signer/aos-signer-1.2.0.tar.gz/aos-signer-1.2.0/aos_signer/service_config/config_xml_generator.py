#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import logging
from aos_signer.service_config.configuration import Configuration
from aos_signer.service_config.keys_manager import KeysManager
from enum import Enum
from lxml.etree import Element, SubElement
from pathlib import PureWindowsPath
from signxml import XMLSigner
from decimal import Decimal

logger = logging.getLogger(__name__)


class ConfigGeneratorException(Exception):
    pass


class ConfigItemType(Enum):
    OBJECT = "object"
    LIST = "list"
    TEXT = "text"


class ConfigXMLGenerator:
    ATTRS = "attrs"
    LIST_ITEM_TAG = "item"
    ITEM_TYPE = "type"
    QUOTA_NAMES_CONVERTER = {
        'cpu': 'cpu_limit',
        'mem': 'memory_limit',
        'state': 'state_disk_limit',
        'storage': 'storage_disk_limit',
        'upload_speed': 'upload_speed_limit',
        'download_speed': 'download_speed_limit',
        'upload': 'upload_limit',
        'download': 'download_limit',
        'temp': 'tmp',
    }

    def __init__(self):
        self._configuration = Configuration()

    def generate(self, file_details) -> Element:
        key_manager = KeysManager()
        certificate = key_manager['meta/' + self._configuration.get_sign_certificate()]
        private_key = key_manager['meta/' + self._configuration.get_sign_key()]
        signed_root = XMLSigner().sign(self._root_element(file_details=file_details), key=private_key, cert=certificate)
        return signed_root

    def _root_element(self, file_details) -> Element:
        root = Element("root")
        root.append(ConfigXMLGenerator._file_details_element(file_details=file_details))
        root.append(self._quotas_element())
        return root

    def _quotas_element(self) -> Element:
        result = Element("quotas")
        quotas = self._configuration.get_quotas()

        if quotas:
            for quota_name, quota_value in quotas.items():
                quota_name = self.QUOTA_NAMES_CONVERTER[quota_name]
                quota_value = str(quota_value)

                if quota_value.lower().endswith('kb'):
                    quota_value = int(float(quota_value.lower().rstrip('kb')) * 1_024)
                elif quota_value.lower().endswith('k'):
                    quota_value = int(float(quota_value.lower().rstrip('k')) * 1_024)
                elif quota_value.lower().endswith('mb'):
                    quota_value = int(float(quota_value.lower().rstrip('mb')) * 1_024 * 1_024)
                elif quota_value.lower().endswith('m'):
                    quota_value = int(float(quota_value.lower().rstrip('m')) * 1_024 * 1_024)
                elif quota_value.lower().endswith('gb'):
                    quota_value = int(float(quota_value.lower().rstrip('gb')) * 1_024 * 1_024 * 1_024)
                elif quota_value.lower().endswith('g'):
                    quota_value = int(float(quota_value.lower().rstrip('g')) * 1_024 * 1_024 * 1_024)

                if quota_name == 'download_speed_limit' or quota_name == 'upload_speed_limit':
                    quota_value = Decimal(quota_value) / Decimal(1_024)

                SubElement(result, quota_name).text = str(quota_value)

        return result

    def _generate_tree(self, key: str, data: dict) -> Element:
        if not isinstance(key, str):
            message = "Info key is not a string, got '{}'.".format(type(key).__name__)
            logger.error(message)
            raise ConfigGeneratorException(message)

        try:
            if isinstance(data, dict):
                attrs = {k: str(v) for k, v in data.get(self.ATTRS, {}).items()}
                attrs[self.ITEM_TYPE] = ConfigItemType.OBJECT.value
                result = Element(key, attrib=attrs)
                for child_key, child_data in data.items():
                    if child_key == self.ATTRS:
                        continue
                    result.append(self._generate_tree(key=child_key, data=child_data))
            elif isinstance(data, list):
                attrs = {"items": self.LIST_ITEM_TAG, self.ITEM_TYPE: ConfigItemType.LIST.value}
                result = Element(key, attrib=attrs)
                for child_data in data:
                    result.append(self._generate_tree(key=self.LIST_ITEM_TAG, data=child_data))
            else:
                attrs = {self.ITEM_TYPE: ConfigItemType.TEXT.value}
                child_data = str(data)
                result = Element(key, attrib=attrs)
                result.text = child_data
        except ValueError:
            message = "Bad key: '{}'.".format(key)
            logger.error(message)
            raise ConfigGeneratorException(message)

        return result

    @staticmethod
    def _file_details_element(file_details) -> Element:
        files = Element("files")
        for fd in file_details:
            SubElement(files, "file", attrib={
                "name": './' + str(PureWindowsPath(fd.name).as_posix()),
                "size": str(fd.size),
                "hash": fd.hash
            })
        return files
