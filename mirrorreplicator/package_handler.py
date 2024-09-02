import lzma
import gzip
from datetime import datetime

class PackageHandler:
  @staticmethod
  def parse_packages_file(file_path):
      packages = []
      current_package = {}

      with open(file_path, 'r') as file:
          for line in file:
              line = line.strip()
              if not line:
                  if current_package:
                      packages.append(current_package)
                      current_package = {}
              else:
                  if ': ' in line:
                      key, value = line.split(': ', 1)
                      current_package[key] = value
                  else:
                      last_key = next(reversed(current_package), None)
                      if last_key:
                          current_package[last_key] += ' ' + line

          if current_package:
              packages.append(current_package)

      return packages

  @staticmethod
  def extract_file(file_path):
      if file_path.endswith(".xz"):
          with lzma.open(file_path, 'rt') as file:
              data = file.read()
      elif file_path.endswith(".gz"):
          with gzip.open(file_path, 'rt') as file:
              data = file.read()
      else:
          with open(file_path, 'r') as file:
              data = file.read()
      
      # Get the current date and time
      current_time = datetime.now()

      # Format the date and time
      formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
      
      print(f"Extracted data from {file_path}")
      print(f"Starting sync at {formatted_time}")


      return data

  @staticmethod
  def find_and_extract_packages(file_list):
      for file_path in file_list:
          if file_path.endswith("Packages") or file_path.endswith("Packages.xz") or file_path.endswith("Packages.gz"):
              data = PackageHandler.extract_file(file_path)
              return PackageHandler.parse_packages_data(data)

  @staticmethod
  def parse_packages_data(data):
      packages = []
      current_package = {}
      lines = data.splitlines()

      for line in lines:
          line = line.strip()
          if not line:
              if current_package:
                  packages.append(current_package)
                  current_package = {}
          else:
              if ': ' in line:
                  key, value = line.split(': ', 1)
                  current_package[key] = value
              else:
                  last_key = next(reversed(current_package), None)
                  if last_key:
                      current_package[last_key] += ' ' + line

      if current_package:
          packages.append(current_package)

      return packages