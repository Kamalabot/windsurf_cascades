from composio import ComposioToolSet, App

# Example usage
toolset = ComposioToolSet(api_key="915sgn0xsfr8web5qwh8")
connection = toolset.get_connected_account("b8821879-e64d-40e4-817d-eb4d77b60160")
print(connection)
