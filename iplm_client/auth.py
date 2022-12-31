import getpass
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport


TOKEN_AUTH_MUTATION = gql(
    """
    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
        payload
        refreshExpiresIn
      }
    }
    """
)


def get_token(username: str, password: str, client: Client) -> str:
    variables = {
        'username': username,
        'password': password,
    }
    result = client.execute(TOKEN_AUTH_MUTATION, variable_values=variables)
    token = result['tokenAuth']['token']
    return token


def get_token_prompt(client: Client) -> str:
    username = input('Enter username:\n')
    password = getpass.getpass(f'Enter password for {username}:\n')

    return get_token(username, password, client)


def get_authenticated_client(url: str = 'http://0.0.0.0:8000/graphql',
                             username: str = None,
                             password: str = None) -> Client:
    """
    Return an authenticated graphQL client

    Args:
        url (str): Url of the graphQL endpoint
        username (str): GraphQL endpoint username
        password (str): GraphQL endpoint password

    Returns:
        GraphQL client
    """

    transport = AIOHTTPTransport(url=url)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    if username is None or password is None:
        token = get_token_prompt(client)
    else:
        token = get_token(username, password, client)

    headers = {'Authorization': f'JWT {token}'}
    transport = AIOHTTPTransport(url=url, headers=headers)
    return Client(transport=transport, fetch_schema_from_transport=True)
