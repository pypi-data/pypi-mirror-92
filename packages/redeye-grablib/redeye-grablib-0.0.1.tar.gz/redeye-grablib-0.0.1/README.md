# GrabLib

A library for retrieving files from HTTP servers.

## Installation

```
pip install redeye-grablib
```

## Usage

```
>>> import grablib
>>> import asyncio
>>>
>>> grabber = grablib.GrabLib()
>>> asyncio.run(grabber.get("https://picsum.photos/20/30"))
{
  'url': 'https://picsum.photos/20/30',
  'sha256': '91aa5c45c2d5709e46631caa743bec9461a4e97df87d60038c126078876add02',
  'data': b'[image binary]'
}
```
