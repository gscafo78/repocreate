#!/usr/bin/python3

import json
import os
import argparse
import logging
import sys
from mirrorreplicator.repository_manage import RepositoryManage


'''
@author: Giovanni SCAFETTA
@version: 0.0.2
@description: This script is realized to clone on line mirrors of a Debian/Ubuntu repository to create your local repository.
@usage: python3 mirep.py -u <url> -p <protocol> -r <rootpath> -d <distributions> -c <components> -a <architectures> -i <inpath> -t <threads> -v
@example: python3 mirep.py -u ftp.debian.org/debian -p http -r /home/user/debian -d bookworm bookworm-updates -c main -a amd64 -i debian -t 4 -v
@license: GLPv3
'''


VERSION = "0.0.2"
FILE_NAME = "repocreate.json"
PATH = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = f"{PATH}/{FILE_NAME}"

class Utilities:
  @staticmethod
  def setup_logging(verbose):
      logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

  @staticmethod
  def accept(question, default_active='n'):
      while True:
          active_input = input(f"{question} ({'Y/n' if default_active == 'y' else 'y/N'})? ").strip().lower()
          if active_input in ['y', 'n', '']:
              return active_input == 'y' or (active_input == '' and default_active == 'y')
          print("Invalid input. Please enter 'y' or 'n'.")

  @staticmethod
  def collect_data(data=None):
      prompts = {
          "proto": "Enter the URL protocol (http/https)",
          "url": "Enter the URL (deb.debian.org)",
          "inpath": "Enter the inpath",
          "distributions": "Enter the distributions (bookworm/bullseye)",
          "components": "Enter the components (main contrib non-free)",
          "architectures": "Enter the architectures (amd64 i386 arm64 armel armhf ppc64el s390x)",
          "rootpath": "Enter the rootpath (/var/www/html)",
          "active": "Active (Y/n)"
      }
      if data is None:
          data = {}
      for key, prompt in prompts.items():
          default = data.get(key, '')
          if key == "active":
              data[key] = Utilities.accept(prompt, 'y' if default else 'n')
              logging.debug("Reading JSON")
          else:
              data[key] = input(f"{prompt} [{default}]: ").strip() or default
      return data

class RepositoryManager:
  def __init__(self, file_path):
      self.file_path = file_path

  def read_json(self):
      if not os.path.exists(self.file_path):
          logging.error(f"Error: The file '{self.file_path}' does not exist.")
          sys.exit(1)  # Exit the program with a non-zero status to indicate an error

      with open(self.file_path, 'r') as file:
          try:
              logging.debug("Reading JSON list file...")
              return json.load(file)
          except json.JSONDecodeError:
              logging.error("Error: Failed to decode JSON. The file may be corrupted.")
              sys.exit(1)  # Exit the program if JSON decoding fails

      return []
  
  def write_to_json(self, data):
      with open(self.file_path, 'w') as file:
          json.dump(data, file, indent=4)

  def add_data(self):
      existing_data = self.read_json()
      new_data = Utilities.collect_data()
      existing_data.append(new_data)
      self.write_to_json(existing_data)
      print(f"Data has been written to {self.file_path}")

  def modify_dictionary(self, data, index, new_dict=None):
      if 0 <= index < len(data):
          if new_dict is not None:
              data[index] = new_dict
          else:
              data.pop(index)
      else:
          raise IndexError("Index out of range")
      return data

  def list_data(self):
      existing_data = self.read_json()
      for index, data in enumerate(existing_data, start=1):
          print(f"Number: {index}")
          for key, value in data.items():
              print(f"{key}: {value}")
          print("="*40)

  def list_url(self):
      existing_data = self.read_json()
      index_width = len(str(len(existing_data)))
      for index, data in enumerate(existing_data, start=1):
          if 'url' in data:
              print(f"[{index:>{index_width}}]: {data['url']}")
      while True:
          try:
              user_input = int(input(f"Select a number between 1 and {len(existing_data)}: "))
              if 1 <= user_input <= len(existing_data):
                  break
              print(f"Please enter a number between 1 and {len(existing_data)}.")
          except ValueError:
              print("Invalid input. Please enter a valid number.")
      selected_data = existing_data[user_input - 1]
      print(f"You selected: {selected_data['url']}")
      return selected_data, user_input - 1

  def edit_data(self):
      selected_data, index_data = self.list_url()
      updated_data = Utilities.collect_data(selected_data)
      existing_data = self.read_json()
      self.modify_dictionary(existing_data, index_data, updated_data)
      self.write_to_json(existing_data)

  def remove_data(self):
      print("Please, select the repository to remove")
      selected_data, index_data = self.list_url()
      if Utilities.accept(f"Are you sure to remove repository n° {index_data + 1} ?", 'n'):
          existing_data = self.read_json()
          self.modify_dictionary(existing_data, index_data)
          self.write_to_json(existing_data)
          print(f"Data has been written to {self.file_path}")

class MirrorRunner:
  def __init__(self, file_path, verbose=False):
      self.file_path = file_path
      self.verbose = verbose

  def parse_json_to_args(self, json_data):
      json_data.pop("active", None)
      
      if isinstance(json_data["distributions"], str):
          json_data["distributions"] = json_data["distributions"].split()

      if isinstance(json_data["components"], str):
          json_data["components"] = json_data["components"].split()

      if isinstance(json_data["architectures"], str):
          json_data["architectures"] = json_data["architectures"].split()

      json_data["verbose"] = self.verbose
      json_data["threads"] = 5
      json_data["remove"] = False

      args = argparse.Namespace(**json_data)
      return args

  def run_mirror(self):
      logging.debug("Starting the mirroring process...")
      repo_manager = RepositoryManager(self.file_path)
      repo_list = repo_manager.read_json()
      for repo in repo_list:
          if repo['active']:
              logging.debug(f"Starting mirroring for {repo['url']}")
              args_ = self.parse_json_to_args(repo)
              logging.debug(args_)
              mirror = RepositoryManage(args_)
              mirror.mirror_repository()

class CLIHandler:
  def __init__(self):
      self.parser = argparse.ArgumentParser(description="Mirror Debian like repositories.")
      self.group = self.parser.add_mutually_exclusive_group()
      self.group.add_argument("--add", action='store_true', help="Add repositories in the database")
      self.group.add_argument("--remove", action='store_true', help="Remove repositories in the database")
      self.group.add_argument("--edit", action='store_true', help="Edit repositories in the database")
      self.group.add_argument("--list", action='store_true', help="Show repositories in the database")
      self.group.add_argument("--run", action='store_true', help="Run the repositories mirroring")
      self.parser.add_argument("--verbose", action='store_true', help="Verbose mode")
      self.parser.add_argument("--version", action='version', version=f"%(prog)s {VERSION}")

  def execute(self, file_path):
      args = self.parser.parse_args()

      # Check if no arguments are passed
      if not any(vars(args).values()):
          self.parser.print_help()
          return

      Utilities.setup_logging(args.verbose)

      repo_manager = RepositoryManager(file_path)
      mirror_runner = MirrorRunner(file_path, args.verbose)

      actions = {
          "add": repo_manager.add_data,
          "list": repo_manager.list_data,
          "edit": repo_manager.edit_data,
          "remove": repo_manager.remove_data,
          "run": mirror_runner.run_mirror
      }

      for action, func in actions.items():
          if getattr(args, action):
              func()
              break

def main():
  cli_handler = CLIHandler()
  try:
      cli_handler.execute(FILE_PATH)
  except KeyboardInterrupt:
      print("\nOperation cancelled by user. Exiting gracefully.")
      exit(0)

if __name__ == "__main__":
  main()