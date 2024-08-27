import argparse
import sys
from .logger import Logger
from .repository_manage import RepositoryManage

VERSION = "0.1.8"

def main():
  parser = argparse.ArgumentParser(description="Mirror a Debian/Ubuntu repository.")
  parser.add_argument("--proto", required=True, help="Protocol to use (e.g., https/http)")
  parser.add_argument("--url", required=True, help="Base URL of the repository (e.g., ftp.debian.org)")
  parser.add_argument("--inpath", required=True, help="Path within the repository (e.g., debian)")
  parser.add_argument("--distributions", required=True, nargs='+', help="List of distributions (e.g., bullseye)")
  parser.add_argument("--components", required=True, nargs='+', help="List of components (e.g., main contrib non-free)")
  parser.add_argument("--architectures", required=True, nargs='+', help="List of architectures (e.g., amd64 i386 arm64 armel armhf ppc64el s390x riscv64)")
  parser.add_argument("--rootpath", required=True, help="Local root path to save files (e.g, /var/www/html/apt)")
  parser.add_argument("--threads", type=int, default=5, help="Number of threads to use (default: 5)")
  parser.add_argument("--remove", action='store_true', help="Remove local repository")
  parser.add_argument("--verbose", action='store_true', help="Verbose mode")
  parser.add_argument("--version", action='version', version=f"%(prog)s {VERSION}")

  try:
      args = parser.parse_args()
  except SystemExit as e:
      print("Error: Missing or invalid arguments.")
      parser.print_help()
      return

  Logger.setup_logging(args.verbose)
  mirror = RepositoryManage(args)

  try:
      if mirror.args.remove:
          mirror.remove_repository()
      else:
          mirror.mirror_repository()
  except KeyboardInterrupt:
      print("\nOperation cancelled by user.")
      sys.exit(0)

if __name__ == "__main__":
  main()