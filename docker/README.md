<img src="https://github.com/gscafo78/repocreate/blob/main/img/RepositoryCreator.jpeg" alt="Repository Creator Logo" width="200" height="200">

Repository Creator Docker Image
====
![Visitor Count](https://visitor-badge.laobi.icu/badge?page_id=gscafo78.repocreate)
[![License: GPL](https://img.shields.io/badge/License-GPL-blue.svg)](https://github.com/gscafo78/repocreate/blob/main/LICENSE)
![Python Version](https://img.shields.io/badge/Python-3.11.2-blue)
[![Email](https://img.shields.io/badge/Email-giovanni.scafetta@gmx.com-blue)](mailto:giovanni.scafetta@gmx.com)


Repository Creator is a image designed to download multiple Debian-like repositories, such as `deb.debian.org` and `archive.ubuntu.com`. It utilizes a JSON file to act as a database for storing the list of repositories.

## Usage

To use the Repository Creator script, follow these steps:

1. Ensure you have docker engine installed on your system (if not you can use this script).
   ```bash
   wget -qO- https://raw.githubusercontent.com/gscafo78/setup/main/inizialsetup/install_docker.sh | bash
   ```
2. Run the docker.
   ```bash
   docker run -d \
        -v /folder/to/save/repositories:/repository \
        -e CRON="* * * * *" 4ss078/repocreate
   ```
3. Show the json file.
   ```bash
   docker exec -it container_id cat /data/repocreate.json
   ```
4. Modify the json file.
   ```bash
   docker exec -it container_id vi /data/repocreate.json
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
    "rootpath": "/repository",
    "active": true
}
```


## Additional Information

- **Contributions**: Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
- **License**: This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
- **Contact**: For questions or support, please contact [giovanni.scafetta@gmx.com](mailto:giovanni.scafetta@gmx.com).