import pytest

import aiostp


@pytest.mark.asyncio
@pytest.fixture(autouse=True)
async def aiostp_configure():
    await aiostp.configure(demo=True)
