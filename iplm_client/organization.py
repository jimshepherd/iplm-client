from typing import Any, List
from gql import Client, gql

from .graphql import GraphQLObject, run_get_query, run_list_query, run_update_mutation


ORGANIZATION_TYPES_QUERY = gql(
    """
    query organizationTypes {
        organizationTypes {
            id
            name
            description
        }
    }
    """
)


UPDATE_ORGANIZATION_TYPE_MUTATION = gql(
    """
    mutation updateOrganizationType($organizationType: OrganizationTypeInput!) {
      updateOrganizationType(organizationType: $organizationType) {
        organizationType {
          id
          name
          description
        }
      }
    }
    """
)


ORGANIZATIONS_QUERY = gql(
    """
    query organizations {
        organizations {
            id
            name
            description
            parent {
                id
                name
            }
            orgTypes {
                id
                name
            }
            addresses {
                street
                street2
                city
                state
                zip
                country
            }
        }
    }
    """
)


UPDATE_ORGANIZATION_MUTATION = gql(
    """
    mutation updateOrganization($organization: OrganizationInput!) {
        updateOrganization(organization: $organization) {
            organization {
                id
                name
                description
                parent {
                    id
                    name
                }
                orgTypes {
                    id
                    name
                }
                addresses {
                    id
                    street
                    street2
                    city
                    state
                    country
                    zip
                }
            }
        }
    }
    """
)


class Address:

    direct_attrs = ['id', 'street', 'street2', 'city', 'state', 'zip', 'country']

    def __init__(self,
                 id: int = None,
                 street: str = None,
                 street2: str = None,
                 city: str = None,
                 state: str = None,
                 zip: str = None,
                 country: str = None):
        self.id = id
        self.street = street
        self.street2 = street2
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country

    @classmethod
    def from_graphql(cls, graphql: dict[str, Any]):
        address = cls()
        for attr in cls.direct_attrs:
            if attr in graphql:
                setattr(address, attr, graphql[attr])
        return address

    def to_graphql(self) -> dict[str, Any]:
        address = {}
        for attr in self.direct_attrs:
            val = getattr(self, attr)
            if val is not None:
                address[attr] = val
        return address


class Organization(GraphQLObject):
    list_query = ORGANIZATIONS_QUERY
    update_mutation = UPDATE_ORGANIZATION_MUTATION

    direct_attrs = ['id', 'name', 'description']
    attr_map: dict[str, Any] = {
        'id': int,
        'name': str,
        'description': str,
        'org_types': lambda: OrganizationType,
    }

    def __init__(self, id: int = None,
                 name: str = None,
                 description: str = None,
                 parent: 'Organization' = None,
                 org_types: List['OrganizationType'] = None,
                 addresses: List[Address] = None):
        self.id = id
        self.name = name
        self.description = description
        self.parent = parent
        self.org_types = org_types
        self.addresses = addresses

    '''
    @classmethod
    def from_graphql(cls, graphql: dict[str, Any]):
        org = cls()
        for attr in cls.direct_attrs:
            if attr in graphql:
                setattr(org, attr, graphql[attr])
        if 'parent' in graphql:
            org.parent = Organization.from_graphql(graphql['parent'])
        if 'orgTypes' in graphql:
            org.org_types = [OrganizationType.from_graphql(g) for g in graphql['orgTypes']]
        if 'addresses' in graphql:
            org.addresses = [Address.from_graphql(g) for g in graphql['addresses']]
        return org

    def to_graphql(self) -> dict[str, Any]:
        org = {}
        for attr in self.direct_attrs:
            val = getattr(self, attr)
            if val is not None:
                org[attr] = val
        if self.parent is not None:
            org['parent'] = self.parent.to_graphql
        if self.org_types is not None:
            org['orgTypes'] = [org_type.to_graphql for org_type in self.org_types]
        if self.addresses is not None:
            org['addresses'] = [address.to_graphql for address in self.addresses]
        return org
    '''

def get_organizations(client: Client) -> List[Organization]:
    result = run_list_query(client, ORGANIZATIONS_QUERY)
    print('result', result)
    orgs_dict = result['organizations']
    if orgs_dict is None:
        return []
    orgs = []
    for org in orgs_dict:
        orgs.append(Organization.from_graphql(org))
    return orgs


def update_organization(client: Client, org: Organization):

    variables = {
        'organization': org.to_graphql()
    }
    print('variables', variables)
    result = run_update_mutation(client, UPDATE_ORGANIZATION_MUTATION, variables)
    updated_org = Organization.from_graphql(result['updateOrganization']['organization'])
    if org.name != updated_org.name:
        print('Organization name not updated')
    print('updated organization', updated_org, updated_org.__dict__)


class OrganizationType:
    list_query = ORGANIZATION_TYPES_QUERY
    update_mutation = UPDATE_ORGANIZATION_TYPE_MUTATION

    direct_attrs = ['id', 'name', 'description']

    def __init__(self, id: int = None,
                 name: str = None,
                 description: str = None):
        self.id = id
        self.name = name
        self.description = description

    @classmethod
    def from_graphql(cls, graphql: dict):
        org_type = cls()
        for attr in cls.direct_attrs:
            if attr in graphql:
                setattr(org_type, attr, graphql[attr])
        return org_type

    def to_graphql(self) -> dict[str, Any]:
        org_type = {}
        for attr in self.direct_attrs:
            val = getattr(self, attr)
            if val is not None:
                org_type[attr] = val
        return org_type


def get_organization_types(client) -> List[OrganizationType]:
    result = run_list_query(client, ORGANIZATION_TYPES_QUERY)
    print('result', result)
    org_types_dict = result['organizationTypes']
    org_types = []
    for org_type in org_types_dict:
        org_types.append(OrganizationType.from_graphql(org_type))
    return org_types


def update_organization_type(client, org_type: OrganizationType):

    variables = {
        'organizationType': {
            'name': org_type.name,
            'description': org_type.description,
        }
    }
    result = run_update_mutation(client, UPDATE_ORGANIZATION_TYPE_MUTATION, variables)
    updated_org_type = OrganizationType.from_graphql(result['updateOrganizationType']['organizationType'])
    if org_type.name != updated_org_type.name:
        print('OrganizationType name not updated')
