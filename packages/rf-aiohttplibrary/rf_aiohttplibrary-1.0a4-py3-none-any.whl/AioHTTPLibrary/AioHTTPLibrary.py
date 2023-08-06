# -*- coding: utf-8 -*-

# Copyright (C) 2021 Joshua Kim Rivera

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# Created by    : Joshua Kim Rivera
# Date          : January 26 2021 15:09 UTC-8

import asyncio
import aiohttp
import logging
from robot.api import logger
from AioHTTPLibrary.version import VERSION

from robotlibcore import (HybridCore,
                          keyword)


__version__ = VERSION

LOGGER = logging.getLogger(__name__)


class AioHTTPLibrary(HybridCore):
    """
    Robotframework Aynschrounous HTTP Library.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        """
        Constructor.
        """
        libraries = []
        HybridCore.__init__(self, libraries)

    @keyword
    def http_test_urls(self, file, slice=5):
        """
        filename: absolute file path to the file containing the urls.
        slice: whatever
        """
        urls = open(file, "r")
        urls = urls.readlines()
        count = len(urls)
        iter = 0
        errors = []
        hop = slice
        while (iter<=count):
            range = (iter+hop) if ((iter+hop) < count) else count
            logger.console(f"\nInitiating Requests Queue Range {iter}-{range}")
            try:
                asyncio.run(self.main(urls[iter:range]))
            except Exception as err:

                errors.append(str(err))
            iter+=hop
        errors = list(filter(None, errors))
        if errors != []:
            raise Exception('\n'.join(errors))

    async def get(
        self,
        session: aiohttp.ClientSession,
        url: str,
        iter,
        **kwargs
        ) -> dict:
        print(f"Requesting {url}")
        url = url.replace('\n', '')
        try:
            resp = await session.get(url)
        except Exception as err:
            return logger.console(str(err) + ' ' + str(resp.status) + str(url))
        if str(resp.status) != '200':
            logger.console(str(resp.status) + ' ' + str(url))
            return str(resp.status) + ' ' + str(url)

    async def gather_with_concurrency(self, n, *tasks):
        semaphore = asyncio.Semaphore(n)

        async def sem_task(task):
            async with semaphore:
                return await task
        return await asyncio.gather(*(sem_task(task) for task in tasks))

    async def main(self, urls, **kwargs):
        # Asynchronous context manager.  Prefer this rather
        # than using a different session for each GET request
        async with aiohttp.ClientSession() as session:
            tasks = []
            iter = 0
            for url in urls:
                iter+=1
                tasks.append(self.get(session=session, url=url, iter=iter, **kwargs))
            # asyncio.gather() will wait on the entire task set to be
            # completed.  If you want to process results greedily as they come in,
            # loop over asyncio.as_completed()
            logs = await self.gather_with_concurrency(100, *tasks)
            res = list(filter(None, logs)) 
            if res is not None:
                raise Exception('\n'.join(res))
            # logger.console('\n'.join(logs))
            # for calls in asyncio.as_completed(tasks):
            #     result = await calls
            #     print(result)
            # results = await asyncio.gather(*tasks, return_exceptions=True)
            # results = asyncio.as_completed(*tasks)
            # file = open('results.txt', 'w+')
            # for result in results:
            #     print(result)
            #     file.write(f"{result}\n")
            # file.close()
        # return htmls


# if __name__ == '__main__':
#     urls = open("urls.txt", "r")
#     urls = urls.readlines()
#     print(urls)
#     # base_url = 'https://pwa.br88uat.com/{url}'
#     # Either take colors from stdin or make some default here
#     count = len(urls)
#     print(count)
#     iter = 0
#     hop = 20
#     while (iter<=count):
#         range = (iter+hop) if ((iter+hop) < count) else count
#         print(f"Range {iter}-{range}")
#         asyncio.run(main(urls[iter:range]))
#         iter+=hop
