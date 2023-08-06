import logging
import json
import aiohttp
from typing import Optional, Dict, List
from .exceptions import DataFinanceClientException, NotFound, ServerError

logger = logging.getLogger(__name__)


class DfClient:
    def __init__(self, host: str, protocol: str = 'http') -> None:
        self.host: str = host
        self.protocol: str = protocol
        self.uri = self.protocol + '://' + self.host

    async def _get_data(self, path: str) -> List:
        uri = self.uri + path
        content = []

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(uri) as response:
                    if response.status >= 200 or response.status <= 299:
                        content = json.loads(await response.text())
                        content = self._prepare_content(content)
                    elif response.status == 404:
                        raise NotFound(f"Not found {uri}")
                    elif response.status >= 500:
                        raise ServerError(f"Server error for {uri}")
                    else:
                        raise DataFinanceClientException(f"Got status {response.status} for {uri}")
        except Exception as e:
            logger.warning(f'Got exception of type {type(e).__name__} in data finance client with message:{e}')

        return content

    def _prepare_content(self, content: Dict) -> List:
        prepared_content = []
        if 'result' in content and 'columns' in content['result'] and 'data' in content['result']:
            columns = [col[0] for col in content['result']['columns']]
            for item in content['result'].get('data', []):
                prepared_content.append({col_name: item[key] for key, col_name in enumerate(columns)})

        return prepared_content

    async def get_simple_intraday_group(
            self,
            group_name: str,
            delay: Optional[int] = None
    ) -> List:
        path = f"/simple/intraday/group/{group_name}"
        if delay is not None:
            path += f"/{delay}"
        return await self._get_data(path)
