# coding: utf-8

"""
    Speech Services API v2.0

    Speech Services API v2.0.  # noqa: E501

    OpenAPI spec version: v2.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import swagger_client
from swagger_client.api.service_health_api import ServiceHealthApi  # noqa: E501
from swagger_client.rest import ApiException


class TestServiceHealthApi(unittest.TestCase):
    """ServiceHealthApi unit test stubs"""

    def setUp(self):
        self.api = swagger_client.api.service_health_api.ServiceHealthApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_health_status(self):
        """Test case for get_health_status

        The action returns the health of the different components of the serivce.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
