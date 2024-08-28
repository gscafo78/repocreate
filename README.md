# Repository Creator

Repository Creator is a script designed to download multiple Debian-like repositories, such as `deb.debian.org` and `archive.ubuntu.com`. It utilizes a JSON file to act as a database for storing the list of repositories.

## Usage

To use the Repository Creator script, follow these steps:

1. Ensure you have Python installed on your system.
2. Prepare the JSON file with the list of repositories you wish to download.
   1. python3 repocreate.py --list to list the repositories
   2. python3 repocreate.py --add to add a repository
3. Run the script using the following command:
   1. python3 repocreate.py --run

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
    "rootpath": "/opt/autofs/mirrorqnap/repository",
    "active": true
}
```

## Additional Information

- **Contributions**: Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
- **License**: This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
- **Contact**: For questions or support, please contact [giovanni.scafetta@gmx.com](mailto:giovanni.scafetta@gmx.com).