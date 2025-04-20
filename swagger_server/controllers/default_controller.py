import connexion
import six

from swagger_server.models.basin import Basin  # noqa: E501
from swagger_server.models.monthly_average import MonthlyAverage  # noqa: E501
from swagger_server.models.station import Station  # noqa: E501
from swagger_server import util


def controller_get_basin_annual_rainfall(basin_id, year):  # noqa: E501
    """Returns total annual rainfall for the specified basin in the specified year

     # noqa: E501

    :param basin_id: 
    :type basin_id: int
    :param year: 
    :type year: int

    :rtype: float
    """
    return 'do some magic!'


def controller_get_basin_details(basin_id):  # noqa: E501
    """Returns complete details of the specified basin

     # noqa: E501

    :param basin_id: 
    :type basin_id: int

    :rtype: Basin
    """
    return 'do some magic!'


def controller_get_basin_monthly_average(basin_id):  # noqa: E501
    """Returns monthly average rainfall for the specified basin across all available years

     # noqa: E501

    :param basin_id: 
    :type basin_id: int

    :rtype: List[MonthlyAverage]
    """
    return 'do some magic!'


def controller_get_basins():  # noqa: E501
    """Returns a list of basins.

     # noqa: E501


    :rtype: List[Basin]
    """
    return 'do some magic!'


def controller_get_station_details(station_id):  # noqa: E501
    """Returns complete details of the specified station

     # noqa: E501

    :param station_id: 
    :type station_id: int

    :rtype: Station
    """
    return 'do some magic!'


def controller_get_stations_in_basin(basin_id):  # noqa: E501
    """Returns a list of stations located within the specified basin.

     # noqa: E501

    :param basin_id: 
    :type basin_id: int

    :rtype: List[Station]
    """
    return 'do some magic!'
