
import os
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from .downloader import Downloader
from .file_manager import FileManager
from .package_handler import PackageHandler

class RepositoryManage:
  def __init__(self, args):
      self.args = args
      self.downloader = Downloader(args.proto, args.url, self.args.rootpath)

  def mirror_repository(self):
      link_list = []
      futures = []
      with ThreadPoolExecutor(max_workers=self.args.threads) as executor:
              
          logging.debug(f"Starting mirror repository for {self.args.url}")
          
          logging.debug(f"Starting mirror distributions for {self.args.distributions}")

          for distribution in self.args.distributions:
              logging.debug(f"Starting mirror distribution for {distribution}")
              for cert in ["InRelease", "Release", "Release.gpg"]:
                  common_path = f"{self.args.url}/{self.args.inpath}/dists/{distribution}/{cert}"
                  futures.append(executor.submit(
                      self.downloader.download_file,
                      f"{self.args.proto}://{common_path}",
                      f"{self.args.rootpath}/{common_path}",
                      "True"
                  ))

              for component in self.args.components:
                  self.downloader.download_directory(f"{self.args.url}/{self.args.inpath}/dists/{distribution}/{component}/i18n/")
                  self.downloader.download_directory(f"{self.args.url}/{self.args.inpath}/dists/{distribution}/{component}/source/")
                  self.downloader.download_directory(f"{self.args.url}/{self.args.inpath}/dists/{distribution}/{component}/cnf/")

                  for arch in self.args.architectures:
                      common_path = f"{self.args.url}/{self.args.inpath}/dists/{distribution}/{component}/Contents-{arch}.gz"
                      futures.append(executor.submit(
                          self.downloader.download_file,
                          f"{self.args.proto}://{common_path}",
                          f"{self.args.rootpath}/{common_path}",
                          "True"
                      ))
                      self.downloader.download_directory(f"{self.args.url}/{self.args.inpath}/dists/{distribution}/{component}/binary-{arch}/")
                      self.downloader.download_directory(f"{self.args.url}/{self.args.inpath}/dists/{distribution}/{component}/debian-installer/binary-{arch}/")
                      save_path = f"{self.args.rootpath}/{self.args.url}/{self.args.inpath}/dists/{distribution}/{component}/binary-{arch}/"
                      pack_files = FileManager.list_files_in_folder(save_path)
                      packages_info = PackageHandler.find_and_extract_packages(pack_files)
                      logging.debug(f"Pages Info: {len(packages_info)}")
                      for index, package in enumerate(packages_info, start=1):
                          logging.debug(f"Serial Number: {index}")
                          logging.debug(f"Package: {package.get('Package')}")
                          logging.debug(f"Version: {package.get('Version')}")
                          logging.debug(f"Description: {package.get('Description')}")
                          logging.debug(f"Filename: {package.get('Filename')}")
                          logging.debug(f"Size: {package.get('Size')}")
                          logging.debug(f"SHA256: {package.get('SHA256')}")
                          downloadlink = f"{self.args.proto}://{self.args.url}/{self.args.inpath}/{package.get('Filename')}"
                          filesave = f"{self.args.rootpath}/{self.args.url}/{self.args.inpath}/{package.get('Filename')}"
                          link_list.append(filesave)
                          if self.args.hash:
                                futures.append(executor.submit(
                                    self.downloader.download_file,
                                    downloadlink,
                                    filesave,
                                    package.get('SHA256'),
                                ))
                          else:
                                futures.append(executor.submit(
                                    self.downloader.download_file,
                                    downloadlink,
                                    filesave,
                                    size=package.get('Size')
                                ))
        
      for future in as_completed(futures):
          future.result()
      logging.debug(f"Mirror cloned successfully.") 

      link_list.extend(self.downloader.get_downloaded_files())
      logging.debug(f"link_list {len(link_list)}")

  def remove_repository(self):
      file_list = []
      for distribution in self.args.distributions:
          for component in self.args.components:
              for arch in self.args.architectures:
                  save_path = f"{self.args.rootpath}/{self.args.url}/{self.args.inpath}/dists/{distribution}/{component}/binary-{arch}/"
                  pack_files = FileManager.list_files_in_folder(save_path)
                  packages_info = PackageHandler.find_and_extract_packages(pack_files)
                  logging.debug(f"Pages Info: {len(packages_info)}")
                  for index, package in enumerate(packages_info, start=1):
                      logging.debug(f"Serial Number: {index}")
                      logging.debug(f"Package: {package.get('Package')}")
                      logging.debug(f"Version: {package.get('Version')}")
                      logging.debug(f"Description: {package.get('Description')}")
                      logging.debug(f"Filename: {package.get('Filename')}")
                      file_list.append(f"{self.args.rootpath}/{self.args.url}/{self.args.inpath}/{package.get('Filename')}")

      print(f"{len(file_list)} files to erase. Continue? (y/N)")
      user_input = input().strip().lower()

      if user_input not in ['y', 'n']:
          user_input = 'n'

      if user_input == 'y':
          for file_path in file_list:
              try:
                  logging.info(f"Deleting: {file_path}")
                  os.remove(file_path)
              except FileNotFoundError:
                  print(f"File not found: {file_path}")
              except PermissionError:
                  print(f"Permission denied: {file_path}")
              except Exception as e:
                  print(f"Error deleting {file_path}: {e}")
          shutil.rmtree(f"{self.args.rootpath}/{self.args.url}/{self.args.inpath}/dists/{distribution}")
      else:
          print("Operation cancelled.")