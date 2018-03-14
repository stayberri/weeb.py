# weeb.py

[![PyPI](https://img.shields.io/pypi/v/weeb.py.svg)](https://pypi.org/project/weeb.py/)
[![PyPI](https://img.shields.io/pypi/pyversions/weeb.py.svg)](https://pypi.org/project/weeb.py/)

An API wrapper in Python for weeb.sh!

Weeb.sh is a private, invite only API for bot developers. In order to use this wrapper, you must have access to the API yourself. If you have access, make sure to replace all instances of "token" with your actual token, such as `Bearer <token>` or `Wolke <token>`, dependent on your token type. Bearer for BearerTokens and Wolke for WolkeTokens.

Please note that the `generate_image`, `generate_status`, `generate_waifu_insult` and `generate_license` functions are locked to certain permission nodes. If you have never asked for these, you probably do not have them.

# Installation
```
pip install weeb.py
```
# Documentation
[Normal docs](https://gist.github.com/DasWolke/f9f8eb7bb9c4faeb10d33ab5bcc95898)\
[Image gen docs](https://gist.github.com/DasWolke/3b1f884ac7779faab7e1026feed78b6c)

# Examples
Note that these functions must be awaited, and thus can only be used inside of an async function.
```python
import weeb

client = weeb.Client(token="token", user_agent="Weeb.py/1.0.4")
                    # User agent is formatted as NAME/VERSION

async def some_async_func_or_event():
    # will print all types
    for t in (await client.get_types()):
        print(t)
        
    # will print all tags
    for t in (await client.get_tags()):
        print(t)
        
    # will request a list of url, id, and filetype of image
    img = await client.get_image(imgtype='bite', nsfw=False, filetype="gif")
    print(img[0])  # prints the image url
    print(img[1])  # prints the image ID
    print(img[2])  # prints the file type
    
    # simple image gen
    # requires simpleimage gen scope. can be awooo, won, or eyes (awooo allows for hair and face as parameters to colour them)
    with open('./path/to/images/file.png', 'wb') as f:
        f.write(await client.generate_image(imgtype='won'))
        f.close()
        # this saves to the path you set it to, even if 'file.png' doesn't exist
        
    # status generation (requires simple image gen scope)
    with open('./path/to/images/file.png', 'wb') as f:
        f.write(await client.generate_status(status='online', avatar='https://cdn.discordapp.com/avatars/267207628965281792/f2f0b2f75710e334095132f33e15bce0.png'))
        f.close()
        # this saves to the path you set it to, even if 'file.png' doesn't exist

        
    # waifu insult (requires waifu image gen scope)
    with open('./path/to/images/file.png', 'wb') as f:
        f.write(await client.generate_waifu_insult(avatar='https://cdn.discordapp.com/avatars/267207628965281792/f2f0b2f75710e334095132f33e15bce0.png'))
        f.close()
        # this saves to the path you set it to, even if 'file.png' doesn't exist
        
    # license generation (requires license image gen scope)
    with open('./path/to/images/file.png', 'wb') as f:
        f.write(await client.generate_license(title="Spook License", avatar="https://imgur.com/zPn0DYT.png", badges=["https://imgur.com/zPn0DYT.png", "https://imgur.com/zPn0DYT.png", "https://imgur.com/zPn0DYT.png"], widgets=["1", "2", "3"]))
        f.close()
        # this saves to the path you set it to, even if 'file.png' doesn't exist
 
```