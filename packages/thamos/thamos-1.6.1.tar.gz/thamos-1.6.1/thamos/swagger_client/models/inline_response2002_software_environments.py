# coding: utf-8

"""
    Thoth User API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 0.6.0-dev

    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class InlineResponse2002SoftwareEnvironments(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        "cuda_version": "str",
        "environment_name": "str",
        "environment_type": "str",
        "image_name": "str",
        "image_sha": "str",
        "os_name": "str",
        "os_version": "str",
        "python_version": "str",
    }

    attribute_map = {
        "cuda_version": "cuda_version",
        "environment_name": "environment_name",
        "environment_type": "environment_type",
        "image_name": "image_name",
        "image_sha": "image_sha",
        "os_name": "os_name",
        "os_version": "os_version",
        "python_version": "python_version",
    }

    def __init__(
        self,
        cuda_version=None,
        environment_name=None,
        environment_type=None,
        image_name=None,
        image_sha=None,
        os_name=None,
        os_version=None,
        python_version=None,
    ):  # noqa: E501
        """InlineResponse2002SoftwareEnvironments - a model defined in Swagger"""  # noqa: E501
        self._cuda_version = None
        self._environment_name = None
        self._environment_type = None
        self._image_name = None
        self._image_sha = None
        self._os_name = None
        self._os_version = None
        self._python_version = None
        self.discriminator = None
        self.cuda_version = cuda_version
        self.environment_name = environment_name
        self.environment_type = environment_type
        self.image_name = image_name
        self.image_sha = image_sha
        self.os_name = os_name
        self.os_version = os_version
        self.python_version = python_version

    @property
    def cuda_version(self):
        """Gets the cuda_version of this InlineResponse2002SoftwareEnvironments.  # noqa: E501

        Cuda version.  # noqa: E501

        :return: The cuda_version of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :rtype: str
        """
        return self._cuda_version

    @cuda_version.setter
    def cuda_version(self, cuda_version):
        """Sets the cuda_version of this InlineResponse2002SoftwareEnvironments.

        Cuda version.  # noqa: E501

        :param cuda_version: The cuda_version of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :type: str
        """
        if cuda_version is None:
            raise ValueError(
                "Invalid value for `cuda_version`, must not be `None`"
            )  # noqa: E501

        self._cuda_version = cuda_version

    @property
    def environment_name(self):
        """Gets the environment_name of this InlineResponse2002SoftwareEnvironments.  # noqa: E501

        Environment name.  # noqa: E501

        :return: The environment_name of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :rtype: str
        """
        return self._environment_name

    @environment_name.setter
    def environment_name(self, environment_name):
        """Sets the environment_name of this InlineResponse2002SoftwareEnvironments.

        Environment name.  # noqa: E501

        :param environment_name: The environment_name of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :type: str
        """
        if environment_name is None:
            raise ValueError(
                "Invalid value for `environment_name`, must not be `None`"
            )  # noqa: E501

        self._environment_name = environment_name

    @property
    def environment_type(self):
        """Gets the environment_type of this InlineResponse2002SoftwareEnvironments.  # noqa: E501

        Environment type.  # noqa: E501

        :return: The environment_type of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :rtype: str
        """
        return self._environment_type

    @environment_type.setter
    def environment_type(self, environment_type):
        """Sets the environment_type of this InlineResponse2002SoftwareEnvironments.

        Environment type.  # noqa: E501

        :param environment_type: The environment_type of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :type: str
        """
        if environment_type is None:
            raise ValueError(
                "Invalid value for `environment_type`, must not be `None`"
            )  # noqa: E501

        self._environment_type = environment_type

    @property
    def image_name(self):
        """Gets the image_name of this InlineResponse2002SoftwareEnvironments.  # noqa: E501

        The name of the image.  # noqa: E501

        :return: The image_name of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :rtype: str
        """
        return self._image_name

    @image_name.setter
    def image_name(self, image_name):
        """Sets the image_name of this InlineResponse2002SoftwareEnvironments.

        The name of the image.  # noqa: E501

        :param image_name: The image_name of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :type: str
        """
        if image_name is None:
            raise ValueError(
                "Invalid value for `image_name`, must not be `None`"
            )  # noqa: E501

        self._image_name = image_name

    @property
    def image_sha(self):
        """Gets the image_sha of this InlineResponse2002SoftwareEnvironments.  # noqa: E501

        The sha value of the image.  # noqa: E501

        :return: The image_sha of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :rtype: str
        """
        return self._image_sha

    @image_sha.setter
    def image_sha(self, image_sha):
        """Sets the image_sha of this InlineResponse2002SoftwareEnvironments.

        The sha value of the image.  # noqa: E501

        :param image_sha: The image_sha of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :type: str
        """
        if image_sha is None:
            raise ValueError(
                "Invalid value for `image_sha`, must not be `None`"
            )  # noqa: E501

        self._image_sha = image_sha

    @property
    def os_name(self):
        """Gets the os_name of this InlineResponse2002SoftwareEnvironments.  # noqa: E501

        The operating system name.  # noqa: E501

        :return: The os_name of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :rtype: str
        """
        return self._os_name

    @os_name.setter
    def os_name(self, os_name):
        """Sets the os_name of this InlineResponse2002SoftwareEnvironments.

        The operating system name.  # noqa: E501

        :param os_name: The os_name of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :type: str
        """
        if os_name is None:
            raise ValueError(
                "Invalid value for `os_name`, must not be `None`"
            )  # noqa: E501

        self._os_name = os_name

    @property
    def os_version(self):
        """Gets the os_version of this InlineResponse2002SoftwareEnvironments.  # noqa: E501

        Operating system version.  # noqa: E501

        :return: The os_version of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :rtype: str
        """
        return self._os_version

    @os_version.setter
    def os_version(self, os_version):
        """Sets the os_version of this InlineResponse2002SoftwareEnvironments.

        Operating system version.  # noqa: E501

        :param os_version: The os_version of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :type: str
        """
        if os_version is None:
            raise ValueError(
                "Invalid value for `os_version`, must not be `None`"
            )  # noqa: E501

        self._os_version = os_version

    @property
    def python_version(self):
        """Gets the python_version of this InlineResponse2002SoftwareEnvironments.  # noqa: E501

        Python version.  # noqa: E501

        :return: The python_version of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :rtype: str
        """
        return self._python_version

    @python_version.setter
    def python_version(self, python_version):
        """Sets the python_version of this InlineResponse2002SoftwareEnvironments.

        Python version.  # noqa: E501

        :param python_version: The python_version of this InlineResponse2002SoftwareEnvironments.  # noqa: E501
        :type: str
        """
        if python_version is None:
            raise ValueError(
                "Invalid value for `python_version`, must not be `None`"
            )  # noqa: E501

        self._python_version = python_version

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(InlineResponse2002SoftwareEnvironments, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, InlineResponse2002SoftwareEnvironments):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
