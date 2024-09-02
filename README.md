<img src="https://github.com/gscafo78/repocreate/blob/main/img/RepositoryCreator.jpeg" alt="Repository Creator Logo" width="200" height="200">

Repository Creator
====
![Visitor Count](https://visitor-badge.laobi.icu/badge?page_id=gscafo78.repocreate)
[![License: GPL](https://img.shields.io/badge/License-GPL-blue.svg)](https://github.com/gscafo78/repocreate/blob/main/LICENSE)
![Python Version](https://img.shields.io/badge/Python-3.11.2-blue)


Repository Creator is a script designed to download multiple Debian-like repositories, such as `deb.debian.org` and `archive.ubuntu.com`. It utilizes a JSON file to act as a database for storing the list of repositories.

## Usage

To use the Repository Creator script, follow these steps:

1. Ensure you have Python installed on your system.
2. Prepare the JSON file with the list of repositories you wish to download.
3. Run the script using the following command:
```bash
python3 repocreate.py --run
```

```bash
$ python3 repocreate.py --help

usage: repocreate [-h] [--add | --remove | --edit | --list | --run] [--verbose] [--version]

Mirror Debian like repositories.

options:
  -h, --help  show this help message and exit
  --add       Add repositories in the database
  --remove    Remove repositories in the database
  --edit      Edit repositories in the database
  --list      Show repositories in the database
  --run       Run the repositories mirroring
  --verbose   Verbose mode
  --version   show program's version number and exit

```


### Installation

```bash
git clone https://github.com/gscafo78/repocreate.git
cd repocreate
pip install -r requirements.txt
```

### JSON File Description

The JSON file should contain a list of repositories in the following format:

```
{
    "proto": "https",
    "url": "deb.debian.org",
    "inpath": "debian",
    "distributions": "bookworm",
    "components": "main contrib non-free non-free-firmware",
    "architectures": "amd64",
    "rootpath": "/your/folder/for/repository",
    "active": true
}
```


## Additional Information

- **Contributions**: Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
- **License**: This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
- **Contact**: For questions or support, please contact [giovanni.scafetta@gmx.com](mailto:giovanni.scafetta@gmx.com).