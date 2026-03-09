from io import BytesIO

import httpx
import numpy as np
from PIL import Image


async def check_tile(*, url: str, transparent_ok: bool = False) -> None:
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

    assert resp.status_code == 200, (  # noqa: PLR2004
        f"HTTP response code {resp.status_code}. Content: {resp.content!r}"
    )

    if not transparent_ok:
        img = Image.open(BytesIO(resp.content))
        alpha = np.array(img.convert("RGBA"))[:, :, 3]

        is_transparent = alpha.max() == 0
        assert not is_transparent, "Tile is fully transparent"


def proxy_url_to_localhost_url(proxy_url: str) -> str:
    return f"http://localhost:{proxy_url.removeprefix('/proxy/')}"
