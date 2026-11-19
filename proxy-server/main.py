
from fastmcp import Client
from fastmcp.server import create_proxy

remote_client = Client(
    "https://absolute-apricot-reptile.fastmcp.app/mcp",
    auth="oauth"
)
mcp = create_proxy(
    remote_client,
    name="Anjali Server Proxy"
)

if __name__ == "__main__":
    mcp.run()
