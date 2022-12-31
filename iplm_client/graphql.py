from gql import Client, gql
from graphql import DocumentNode, ExecutionResult
from typing import Any


def snake_to_camel_case(input: str) -> str:
    words = input.split('_')
    return words[0] + ''.join(word.title() for word in words[1:])


class GraphQLObject:

    attr_map: dict[str, Any] = {
        'id': int,
    }

    def __init__(self, id: int = None):
        self.id = id

    @classmethod
    def from_graphql(cls, graphql: dict[str, Any]):

        item = cls()
        for attr_name, attr_type in cls.attr_map.items():
            graphql_attr_name = snake_to_camel_case(attr_name)
            if graphql_attr_name in graphql:
                value = graphql[graphql_attr_name]
                if isinstance(value, list):
                    values = []
                    for val in value:
                        try:
                            values.append(attr_type.from_graphql(val))
                        except:
                            values.append(val)
                            print('from_graphql exception', e)
                        setattr(item, attr_name, values)
                else:
                    try:
                        setattr(item, attr_name, attr_type.from_graphql(value))
                    except:
                        setattr(item, attr_name, value)
        return item

    def to_graphql(self) -> dict[str, Any]:
        item_dict = {}
        for attr_name, attr_type in self.attr_map.items():
            value = getattr(self, attr_name)
            if value is not None:
                graphql_attr_name = snake_to_camel_case(attr_name)
                if isinstance(value, list):
                    values = []
                    for val in value:
                        try:
                            values.append(val.to_graphql())
                        except Exception as e:
                            print('to_graphql exception', e)
                            values.append(val)
                    item_dict[graphql_attr_name] = values
                else:
                    try:
                        item_dict[graphql_attr_name] = value.to_graphql()
                    except:
                        item_dict[graphql_attr_name] = value
        return item_dict


def run_update_mutation(client: Client,
                        mutation: DocumentNode,
                        variables: dict[str, Any] | None = None
                        ) -> dict[str, Any] | ExecutionResult:
    result = client.execute(mutation, variable_values=variables)
    print(result)
    return result


def run_get_query(client: Client,
                  query: DocumentNode,
                  variables: dict[str, Any] | None = None
                  ) -> dict[str, Any] | ExecutionResult:
    result = client.execute(query, variable_values=variables)
    print(result)
    return result


def run_list_query(client: Client,
                   query: DocumentNode,
                   variables: dict[str, Any] | None = None
                   ) -> dict[str, Any] | ExecutionResult:
    result = client.execute(query, variable_values=variables)
    print(result)
    return result
