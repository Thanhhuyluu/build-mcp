import logging
import shutil
import subprocess
from typing import Annotated
from fastmcp import FastMCP

import os

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(message)s")
logger = logging.getLogger("DestopController")
logger.setLevel(logging.INFO)


mcp = FastMCP("Desktop Controll")

@mcp.tool

async def open_zen_browser(
    url: Annotated[
        str | None,
        "URL cần mở, ví dụ https://google.com. Bỏ trống để chỉ mở Zen Browser."
    ] = None,
) -> str:
    # Tùy máy, executable có thể là zen-browser hoặc zen
    zen_cmd = shutil.which("zen-browser") or shutil.which("zen")

    if not zen_cmd:
        return (
            "Không tìm thấy Zen Browser trong PATH. "
            "Hãy chạy `which zen-browser` hoặc `which zen` để kiểm tra."
        )

    try:
        cmd = [zen_cmd]

        if url:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            cmd.append(url)

        env = os.environ.copy()

        subprocess.Popen(
            cmd,
            env=env,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return f"Đã mở Zen Browser{' tại ' + url if url else ''}."

    except Exception as e:
        return f"Không thể mở Zen Browser: {e}"
if __name__ == "__main__":
    logger.info("Store MCP server starting (HTTP mode on port 8420)")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8420)



