

from typing import Callable, List
from gaia_sdk.api.VariableRegistry import VariableRegistry
from gaia_sdk.graphql.request.enumeration.Order import Order
from gaia_sdk.graphql.request.enumeration.OrderByField import OrderByField
from gaia_sdk.graphql.request.enumeration.EdgeOrderByField import EdgeOrderByField
from gaia_sdk.graphql.request.enumeration.EdgeType import EdgeType


class UpdateRoleImpulse():
    """
    The specification to update a role instance
    """
    roleId: str
    name: str
    permissions: List[str]

    def __init__(self, roleId: str, name: str, permissions: List[str]):
        self.roleId = roleId
        self.name = name
        self.permissions = permissions

    def __eq__(self, other):
        if type(other) is type(self):
            return self.roleId == other.roleId and self.name == other.name and self.permissions == other.permissions
        return False

    def __repr__(self):
        return {'roleId': self.roleId, 'name': self.name, 'permissions': self.permissions}
