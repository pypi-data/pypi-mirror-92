# HostnameResolver

## Description
This package implement netbios and LLMNR query tool in python and HostnameResolver command line tool.

## Requirements
This package require : 
 - python3
 - python3 Standard Library
 - Scapy

## Installation
```bash
pip install LocalResolver 
```

## Examples

### Command lines
```bash
HostnameResolver -h
HostnameResolver 192.168.1.2
HostnameResolver 192.168.1.3,192.168.1.2,WIN10,HOMEPC,example.com
```

### Python3
```python
from LocalResolver import LocalResolver

localResolver = LocalResolver("192.168.1.45", timeout=3)
hostname = localResolver.resolve_NBTNS()
hostname = localResolver.resolve_LLMNR()
```

## Link
[Github Page](https://github.com/mauricelambert/LocalResolver)

## Licence
Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
