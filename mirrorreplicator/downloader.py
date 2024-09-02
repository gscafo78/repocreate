import os
import subprocess
import requests
from tqdm import tqdm
import logging
import hashlib


class Downloader:
  def __init__(self, proto, url, rootpath):
      self.proto = proto
      self.url = url
      self.rootpath = rootpath
      self.downloaded_files = []
      self.downloaded_count = 0
      self.skipped_count = 0

  def verify_file_hash(file_path, hash_string):
    """
    Verifies if the SHA-256 hash of the file matches the provided hash string.
    param file_path: Path to the file.
    :param hash_string: SHA-256 hash string to compare against.
    :return: True if the file's hash matches the provided hash string, False otherwise.
    """
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as file:
            while chunk := file.read(8192):
                sha256.update(chunk)
        
        file_hash = sha256.hexdigest()
        
        return file_hash == hash_string
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False



  def download_directory(self, path, exclude_pattern="index.html*"):
      parsed_url = path.split('/')[0]
      command = [
          "wget", "-r", "-np", "-nH",
          "-P", f"{self.rootpath}/{parsed_url}",
          "--reject", exclude_pattern, f"{self.proto}://{path}"
      ]
      try:
          with open(os.devnull, 'w') as devnull:
              subprocess.run(command, check=True, stdout=devnull, stderr=devnull)
          logging.debug(f"Download completed successfully for {path}")
          self._add_downloaded_files_from_directory(path)
      except subprocess.CalledProcessError as e:
          if e.returncode == 8:
              logging.debug(f"File does not exist: {path}")
          else:
              logging.error(f"An error occurred: {e}")

  def download_file(self, path, full_path, hash_string=None):
      """
      Downloads a single file from the specified path.

      Parameters:
      path (str): The URL of the file to download.
      full_path (str): The full path where the file will be saved.
      overwrite (bool): Whether to overwrite the file if it already exists.
      """
      folder = os.path.dirname(full_path)
      if not os.path.exists(folder):
          os.makedirs(folder, exist_ok=True)
          logging.debug(f"Created directory: {folder}")

      file_name = os.path.basename(full_path)
      if os.path.exists(full_path) and hash_string is not None:
    #   if os.path.exists(full_path) and not overwrite:
          if Downloader.verify_file_hash(full_path, hash_string):
            logging.debug(f"File '{file_name}' already exists. Skipping download.")
            self.skipped_count += 1  # Increment skipped count
            return
          elif hash_string != " True" :
              logging.info(f"File '{file_name}' already exists but hash does not match. Overwriting.")

      try:
          # Request the file from the URL
          response = requests.get(path, stream=True)
          response.raise_for_status()
          total_size = int(response.headers.get('content-length', 0))
          with open(full_path, 'wb') as file, tqdm(
              desc=file_name,
              total=total_size,
              unit='B',
              unit_scale=True,
              unit_divisor=1024
          ) as bar:
              for chunk in response.iter_content(chunk_size=8192):
                  file.write(chunk)
                  bar.update(len(chunk))
          logging.debug(f"File '{file_name}' downloaded successfully.")
          self.downloaded_files.append(full_path)  # Add to the list
          self.downloaded_count += 1  # Increment downloaded count
      
      except requests.exceptions.HTTPError as e:
          if response.status_code == 404:
              logging.debug(f"Failed to download the file: {e}")
          else:
              logging.error(f"An error occurred: {e}")



  def _add_downloaded_files_from_directory(self, path):
      for root, _, files in os.walk(f"{self.rootpath}/{path}"):
          for file in files:
              self.downloaded_files.append(os.path.join(root, file))

  def get_downloaded_files(self):
      return self.downloaded_files

  def get_downloaded_count(self):
      return self.downloaded_count

  def get_skipped_count(self):
      return self.skipped_count