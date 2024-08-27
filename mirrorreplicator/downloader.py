import os
import subprocess
import requests
from tqdm import tqdm
import logging

class Downloader:
  def __init__(self, proto, url, rootpath):
      self.proto = proto
      self.url = url
      self.rootpath = rootpath
      self.downloaded_files = []
      self.downloaded_count = 0
      self.skipped_count = 0

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

  def download_file(self, path, full_path, overwrite=False):
      folder = os.path.dirname(full_path)
      if not os.path.exists(folder):
          os.makedirs(folder, exist_ok=True)
          logging.debug(f"Created directory: {folder}")

      file_name = os.path.basename(full_path)
      if os.path.exists(full_path) and not overwrite:
          logging.debug(f"File '{file_name}' already exists. Skipping download.")
          self.skipped_count += 1
          return

      try:
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
          self.downloaded_files.append(full_path)
          self.downloaded_count += 1
      except requests.exceptions.HTTPError as e:
          if response.status_code == 404:
              logging.error(f"Failed to download the file: {e}")
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