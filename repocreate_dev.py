#!/usr/bin/python3

import json
import os
import argparse
import logging

VERSION = "0.0.1"
FILE_NAME = "repocreate.json"
PATH = "/opt/github/03_Script/Python/repocreate"
FILE_PATH = f"{PATH}/{FILE_NAME}"

def setup_logging(verbose):
  logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

def accept(question, default_active='n'):
  while True:
      active_input = input(f"{question} ({'Y/n' if default_active == 'y' else 'y/N'})? ").strip().lower()
      if active_input in ['y', 'n', '']:
          return active_input == 'y' or (active_input == '' and default_active == 'y')
      print("Invalid input. Please enter 'y' or 'n'.")

def collect_data(data=None):
  prompts = {
      "protocol": "Enter the URL protocol (http/https)",
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
          data[key] = accept(prompt, 'y' if default else 'n',)
      else:
          data[key] = input(f"{prompt} [{default}]: ").strip() or default
  return data

def read_json(file_path):
  if os.path.exists(file_path):
      with open(file_path, 'r') as file:
          try:
              return json.load(file)
          except json.JSONDecodeError:
              return []
  return []

def write_to_json(file_path, data):
  with open(file_path, 'w') as file:
      json.dump(data, file, indent=4)

def add_data(file_path):
  existing_data = read_json(file_path)
  new_data = collect_data()
  existing_data.append(new_data)
  write_to_json(file_path, existing_data)
  print(f"Data has been written to {file_path}")

def modify_dictionary(data, index, new_dict=None):
  if 0 <= index < len(data):
      if new_dict is not None:
          data[index] = new_dict
      else:
          data.pop(index)
  else:
      raise IndexError("Index out of range")
  return data

def list_data(file_path):
  existing_data = read_json(file_path)
  for index, data in enumerate(existing_data, start=1):
      print(f"Number: {index}")
      for key, value in data.items():
          print(f"{key}: {value}")
      print("="*40)

def list_url(file_path):
  existing_data = read_json(file_path)
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

def edit_data(file_path):
  selected_data, index_data = list_url(file_path)
  updated_data = collect_data(selected_data)
  existing_data = read_json(file_path)
  modify_dictionary(existing_data, index_data, updated_data)
  write_to_json(file_path, existing_data)

def remove_data(file_path):
  print("Please, select the repository to remove")
  selected_data, index_data = list_url(file_path)
  if accept(f"Are you sure to remove repository n° {index_data + 1} ?", 'n'):
      existing_data = read_json(file_path)
      modify_dictionary(existing_data, index_data)
      write_to_json(file_path, existing_data)
      print(f"Data has been written to {file_path}")

def run_mirror():
   
   return

def main():
  parser = argparse.ArgumentParser(description="Mirror Debian like repositories.")
  group = parser.add_mutually_exclusive_group()
  group.add_argument("--add", action='store_true', help="Add repositories in the database")
  group.add_argument("--remove", action='store_true', help="Remove repositories in the database")
  group.add_argument("--edit", action='store_true', help="Edit repositories in the database")
  group.add_argument("--list", action='store_true', help="Show repositories in the database")
  group.add_argument("--run", action='store_true', help="Run the repositories mirroring")
  parser.add_argument("--verbose", action='store_true', help="Verbose mode")
  parser.add_argument("--version", action='version', version=f"%(prog)s {VERSION}")

  args = parser.parse_args()
  setup_logging(args.verbose)

  actions = {
      "add": add_data,
      "list": list_data,
      "edit": edit_data,
      "remove": remove_data
      "run": run_mirror
  }

  for action, func in actions.items():
      if getattr(args, action):
          func(FILE_PATH)
          break

if __name__ == "__main__":
  main()