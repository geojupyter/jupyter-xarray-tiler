from jupyter_server_titiler.constants import ENDPOINT_BASE


async def test_extension_root_route(jp_fetch):
    # Not sure why a 2nd argument is needed! ¯\_(ツ)_/¯
    response = await jp_fetch(ENDPOINT_BASE, "/")

    assert response.code == 200
    assert (
        response.body
        == b"This is the root endpoint of the 'jupyter_server_titiler' server extension"
    )
