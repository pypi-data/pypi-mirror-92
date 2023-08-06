# MIT License
#
# Copyright (c) 2021 DTOG
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import aiohttp
from .endpoints import devurl as url

async def get_status():
    async with aiohttp.ClientSession() as cs:
        async with cs.get(await url("status")) as p:
            json = await p.json()
            return list(json)[0]

async def lastseen(user):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(await url(f"seen?username={user}")) as l:
            lastseenapi = await l.json()
            return lastseenapi[0]['seen']


async def get_prioq():
    async with aiohttp.ClientSession() as cs:
        async with cs.get(await url("prioq")) as p:
            json = await p.json()
            return list(json)


async def get_stats(user):
    try:
        async with aiohttp.ClientSession() as cs:
            async with cs.get(await url(f"stats?username={user}")) as l:
                return (await l.json())[0]
    except IndexError:
        return None


async def get_death(user):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(await url(f"stats?lastdeath={user}")) as l:
            return (await l.json())[0]


async def get_kill(user):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(await url(f"stats?lastkill={user}")) as l:
            return (await l.json())[0]


class priorityqueue(object):
    @staticmethod
    async def length():
        return int((await get_prioq())[1])

    @staticmethod
    async def time():
        return (await get_prioq())[2]


class userstats(object):
    @staticmethod
    async def kills(user):
        try:
            return (await get_stats(user))['kills']
        except Exception:
            return None

    @staticmethod
    async def deaths(user):
        return (await get_stats(user))['deaths']

    @staticmethod
    async def joins(user):
        return (await get_stats(user))['joins']

    @staticmethod
    async def leaves(user):
        return (await get_stats(user))['leaves']

    @staticmethod
    async def id(user):
        return (await get_stats(user))['id']

    @staticmethod
    async def adminlevel(user):
        return (await get_stats(user))['adminlevel']

    @staticmethod
    async def uuid(user):
        return (await get_stats(user))['uuid']


class lastdeath(object):
    @staticmethod
    async def id(user):
        try:
            return (await get_death(user))['id']
        except Exception:
            return None

    @staticmethod
    async def datetime(user):
        try:
            return (await get_death(user))['date'] + " " + (await get_death(user))['time']
        except Exception:
            return None

    @staticmethod
    async def message(user):
        try:
            return str((await get_death(user))['message'])
        except Exception:
            return None


class lastkill(object):
    @staticmethod
    async def id(user):
        try:
            return (await get_kill(user))['id']
        except Exception:
            return None

    @staticmethod
    async def datetime(user):
        try:
            return (await get_kill(user))['date'] + " " + (await get_death(user))['time']
        except Exception:
            return None

    @staticmethod
    async def message(user):
        try:
            return str((await get_kill(user))['message'])
        except Exception:
            return None

async def tps():
    return (await get_status())[0]

async def uptime():
    return (await get_status())[3]