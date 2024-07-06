from urllib.parse import urlparse
import os


def update_m3u8_content(play_url: str, m3u8_content: str, is_proxy: bool = False) -> str:
    parsed_url = urlparse(play_url)
    port = parsed_url.port if parsed_url.port else (443 if parsed_url.scheme == "https" else 80)
    domain_port = f"{parsed_url.hostname}:{port}"
    path = "/".join(parsed_url.path.split("/")[:-1])

    lines = m3u8_content.strip().splitlines()
    modified_lines = []

    PROXY_URL = os.getenv("PROXY_URL", "") if is_proxy else ""

    for line in lines:
        if line and not line.startswith("#"):
            parsed_line_url = urlparse(line)
            if not parsed_line_url.netloc:
                modified_line = f"{PROXY_URL}/data/{domain_port}{path}/{line}"
            else:
                modified_line = f"{PROXY_URL}/data/{parsed_line_url.hostname}:{parsed_line_url.port or (443 if parsed_line_url.scheme == 'https' else 80)}{parsed_line_url.path}{line[line.find('/', line.find('//') + 2)]}"
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)

    return "\n".join(modified_lines)
