# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.basin import Basin  # noqa: E501
from swagger_server.models.monthly_average import MonthlyAverage  # noqa: E501
from swagger_server.models.station import Station  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_controller_get_basin_annual_rainfall(self):
        """Test case for controller_get_basin_annual_rainfall

        Returns total annual rainfall for the specified basin in the specified year
        """
        response = self.client.open(
            '/rain-api/v2/basins/{basinId}/annualRainfalls/{year}'.format(basin_id=56, year=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_basin_details(self):
        """Test case for controller_get_basin_details

        Returns complete details of the specified basin
        """
        response = self.client.open(
            '/rain-api/v2/basins/{basinId}'.format(basin_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_basin_monthly_average(self):
        """Test case for controller_get_basin_monthly_average

        Returns monthly average rainfall for the specified basin across all available years
        """
        response = self.client.open(
            '/rain-api/v2/basins/{basinId}/monthlyAverage'.format(basin_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_basins(self):
        """Test case for controller_get_basins

        Returns a list of basins.
        """
        response = self.client.open(
            '/rain-api/v2/basins',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_station_details(self):
        """Test case for controller_get_station_details

        Returns complete details of the specified station
        """
        response = self.client.open(
            '/rain-api/v2/stations/{stationId}'.format(station_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_stations_in_basin(self):
        """Test case for controller_get_stations_in_basin

        Returns a list of stations located within the specified basin.
        """
        response = self.client.open(
            '/rain-api/v2/stationsInBasin/{basinId}'.format(basin_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
