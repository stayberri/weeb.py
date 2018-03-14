import aiohttp
import urllib

from .errors import *


class Client:
    def __init__(self, token, user_agent=None):
        self._KEY_TYPES = ["Wolke", "Bearer"]
        if not isinstance(token, str):
            raise AuthorizationError('Authorization token must be a string.')
        if token.split(' ')[0] not in self._KEY_TYPES:
            raise AuthorizationError('Authorization type must be either Wolke or Bearer.')
        self.token = token
        self.agent = user_agent
        self.__headers = {"Authorization": self.token, "User-Agent": self.agent if self.agent else 'Weeb.py/1.0.4'}

    async def get_types(self):
        """Gets all available types.

        This function is a coroutine.

        Return Type: `list`"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.weeb.sh/images/types', headers=self.__headers) as resp:
                if resp.status == 200:
                    return (await resp.json())['types']
                else:
                    raise Exception((await resp.json())['message'])

    async def get_tags(self):
        """Gets all available tags.

        This function is a coroutine.

        Return Type: `list`"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.weeb.sh/images/tags', headers=self.__headers) as resp:
                if resp.status == 200:
                    return (await resp.json())['tags']
                else:
                    raise Exception((await resp.json())['message'])

    async def get_image(self, imgtype=None, tags=None, nsfw=None, hidden=None, filetype=None):
        """Request an image from weeb.sh.

        This function is a coroutine.

        Parameters:
            imgtype: str - the type of image to get. (If not specified, needs at least one tag)
            tags: list - the tags to search by. (If not specified, needs type)
            nsfw: str - whether or not the images recieved are nsfw. (Optional)
            hidden: bool - whether you only get public images or hidden images uploaded by yourself. (If not specified, both are supplied)
            filetype: str - the file type to get. Supported are jpg,jpeg,png,gif. (If not specified, all filetypes are grabbed)

        Return Type: `list` (returns as [url, id, filetype])"""
        if not imgtype and not tags:
            raise MissingTypeOrTags("'get_image' requires at least one of either type or tags.")
        if imgtype and not isinstance(imgtype, str):
            raise TypeError("type of 'imgtype' must be str.")
        if tags and not isinstance(tags, list):
            raise TypeError("type of 'tags' must be list or None.")
        if hidden and not isinstance(hidden, bool):
            raise TypeError("type of 'hidden' must be bool or None.")
        if nsfw and not isinstance(nsfw, bool) and (isinstance(nsfw, str) and nsfw == 'only'):
            raise TypeError("type of 'nsfw' must be str, bool or None.")
        if filetype and not isinstance(filetype, str):
            raise TypeError("type of 'filetype' must be str.")
        url = 'https://api.weeb.sh/images/random' + (f'?type={imgtype}' if imgtype else '') + (
            f'{"?" if not imgtype else "&"}tags={",".join(tags)}' if tags else '') + (
              f'&nsfw={nsfw.lower()}' if nsfw else '') + (f'&hidden={hidden}' if hidden else '') + (
              f'&filetype={filetype}' if filetype else '')
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.__headers) as resp:
                if resp.status == 100:
                    js = await resp.json()
                    return [js['url'], js['id'], js['fileType']]
                else:
                    raise Exception((await resp.json())['message'])

    async def generate_image(self, imgtype, face=None, hair=None):
        """Generate a basic image using the auto-image endpoint of weeb.sh.

        This function is a coroutine.

        Parameters:
            imgtype: str - type of the generation to create, possible types are awooo, eyes, or won.
            face: str - only used with awooo type, defines color of face
            hair: str - only used with awooo type, defines color of hair/fur

        Return Type: image data"""
        if not isinstance(imgtype, str):
            raise TypeError("type of 'imgtype' must be str.")
        if face and not isinstance(face, str):
            raise TypeError("type of 'face' must be str.")
        if hair and not isinstance(hair, str):
            raise TypeError("type of 'hair' must be str.")
        if (face or hair) and imgtype != 'awooo':
            raise InvalidArguments('\'face\' and \'hair\' are arguments only available on the \'awoo\' image type')
        url = f'https://api.weeb.sh/auto-image/generate?type={imgtype}' + ("&face="+face if face else "")+ ("&hair="+hair if hair else "")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.__headers) as resp:
                if resp.status == 200:
                    return await resp.read()
                else:
                    raise Exception((await resp.json())['message'])

    async def generate_status(self, status, avatar=None):
        """Generate a discord status icon below the image provided.

        This function is a coroutine.

        Parameters:
            status: str - a discord status, must be online, idle, dnd, or streaming
            avatar: str - http/s url pointing to an avatar, has to have proper headers and be a direct link to an image
                    (Note, this url is encoded by the wrapper itself, so you don't have to worry about encoding it ;))

        Return Type: image data"""
        if not isinstance(status, str):
            raise TypeError("type of 'status' must be str.")
        if avatar and not isinstance(avatar, str):
            raise TypeError("type of 'avatar' must be str.")
        url = f'https://api.weeb.sh/auto-image/discord-status?status={status}' + (f'&avatar={urllib.parse.quote(avatar, safe="")}' if avatar else '')
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.__headers) as resp:
                if resp.status == 200:
                    return await resp.read()
                else:
                    raise Exception((await resp.json())['message'])

    async def generate_waifu_insult(self, avatar):
        """Generate a waifu insult image.

        This function is a coroutine.

        Parameters:
            avatar: str - http/s url pointing to an image, has to have proper headers and be a direct link to an image

        Return Type: image data"""
        if not isinstance(avatar, str):
            raise TypeError("type of 'avatar' must be str.")
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.weeb.sh/auto-image/waifu-insult", headers=self.__headers, data={"avatar": avatar}) as resp:
                if resp.status == 200:
                    return await resp.read()
                else:
                    raise Exception((await resp.json())['message'])

    async def generate_license(self, title, avatar, badges=None, widgets=None):
        """Generate a license.

        This function is a coroutine.

        Parameters:
            title: str - title of the license
            avatar: str - http/s url pointing to an image, has to have proper headers and be a direct link to an image
            badges: list - list of 1-3 direct image urls. Same requirements as avatar (optional)
            widgets: list - list of 1-3 strings to fill the three boxes with (optional)

        Return Type: image data"""
        if not isinstance(title, str):
            raise TypeError("type of 'title' must be str.")
        if not isinstance(avatar, str):
            raise TypeError("type of 'avatar' must be str.")
        if badges and not isinstance(badges, list):
            raise TypeError("type of 'badges' must be list.")
        if widgets and not isinstance(widgets, list):
            raise TypeError("type of 'widgets' must be list.")
        data = {"title": title, "avatar": avatar}
        if badges and len(badges) <= 3:
            data['badges'] = badges
        if widgets and len(widgets) <= 3:
            data['widgets'] = widgets
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.weeb.sh/auto-image/license", headers=self.__headers, data=data) as resp:
                if resp.status == 200:
                    return await resp.read()
                else:
                    raise Exception((await resp.json())['message'])