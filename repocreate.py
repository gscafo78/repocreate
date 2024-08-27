#!/usr/bin/python3

import json
import os
import argparse
from mirrorreplicator import Logger
import logging


'''
@author: Giovanni SCAFETTA
@version: 0.0.1
@description: This script is realized to clone an on line mirror of a Debian like repositories to create your local repository.
@usage: python3 
@example: python3 
@license: GLPv3
'''
VERSION = "0.0.1"

file_name = "repocreate.json"
path = "/opt/github/03_Script/Python/repocreate"
file_path =f"{path}/{file_name}"



def collect_data(data=None):
  
  if data is None:
    # Prompt the user for each piece of data
    protocol = input("Enter the URL protocol (http/https): ")
    url = input("Enter the URL (deb.debian.org): ")
    inpath = input("Enter the inpath: ")
    distributions = input("Enter the distributions (bookworm/bullseye): ")
    components = input("Enter the components (main contrib non-free): ")
    architectures = input("Enter the architectures (amd64 i386 arm64 armel armhf ppc64el s390x): ")
    rootpath = input("Enter the rootpath (/var/www/html): ")
    # Validate the 'active' input
    while True:
        active_ = input("Active (Y/n)? ").strip()
        if active_ == '':
            active_ = 'y'  # Set default value
        if active_.lower() in ['y', 'n']:
            break
        else:
            print("Invalid input. Please enter 'y', 'Y', 'n', or 'N'.")

    if active_ == 'y':
        active = True
    else:
        active = False

  else:
    
    # Prompt the user for each piece of data, allowing for default values
    protocol = input(f"Enter the URL protocol (http/https) [{data['protocol']}]: ") or data['protocol']
    url = input(f"Enter the URL [{data['url']}]: ") or data['url']
    inpath = input(f"Enter the inpath [{data['inpath']}]: ") or data['inpath']
    distributions = input(f"Enter the distributions (bookworm/bullseye) [{data['distributions']}]: ") or data['distributions']
    components = input(f"Enter the components (main contrib non-free) [{data['components']}]: ") or data['components']
    architectures = input(f"Enter the architectures (amd64 i386 arm64 armel armhf ppc64el s390x) [{data['architectures']}]: ") or data['architectures']
    rootpath = input(f"Enter the rootpath [{data['rootpath']}]: ") or data['rootpath']
    # Validate the 'active' input with a default value
    while True:
        # Convert the boolean to 'Y' or 'N' for the prompt
        default_active = 'Y' if data['active'] else 'N'
        
        # Prompt the user, using the string representation of the boolean
        active_ = input(f"Active (Y/n) [{default_active}]? ").strip().upper() or default_active
        
        # Check if the input is valid
        if active_ in ['Y', 'N']:
            break
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

    # Convert the input back to a boolean
    active = active_ == 'Y'

  # Store the data in a dictionary

  data = {
      "protocol": protocol,
      "url": url,
      "inpath": inpath,
      "distributions": distributions,
      "components": components,
      "architectures": architectures,
      "rootpath": rootpath,
      "active": active
  }

  return data


def read_json(file_path):
  # Read the existing data from the JSON file
  if os.path.exists(file_path):
      with open(file_path, 'r') as file:
          try:
              return json.load(file)
          except json.JSONDecodeError:
              return []
  return []

def write_to_json(file_path, data):
  # Write the list of dictionaries to a JSON file
  with open(file_path, 'w') as file:
      json.dump(data, file, indent=4)

def add_data(file_path):
       # Read existing data
    existing_data = read_json(file_path)

    # Collect new data from the user
    new_data = collect_data()

    # Append the new data to the existing data
    existing_data.append(new_data)

    # Write the updated data to the JSON file
    write_to_json(file_path, existing_data)

    print(f"Data has been written to {file_path}")


def list_data(file_path):
  # Read the existing data from the JSON file
  existing_data = read_json(file_path)
  # Print the list of dictionaries
  for index, data in enumerate(existing_data, start=1):
    print(f"Number: {index}")
    for key, value in data.items():
        print(f"{key}: {value}")
    print("="*40)
    print()

def list_url(file_path):
  # Read the existing data from the JSON file
  existing_data = read_json(file_path)
  # Determine the width for the index based on the number of entries
  index_width = len(str(len(existing_data)))
  # Print the list of URLs with improved tabulation
  for index, data in enumerate(existing_data, start=1):
      if 'url' in data:
          print(f"[{index:>{index_width}}]: {data['url']}")
  print()
  
  # Prompt the user to select a number
  while True:
      try:
          user_input = int(input(f"Select a number between 1 and {index}: "))
          if 1 <= user_input <= index:
              break  # Valid input, exit the loop
          else:
              print(f"Please enter a number between 1 and {index}.")
      except ValueError:
          print("Invalid input. Please enter a valid number.")
  
  # Process the validated input
  selected_data = existing_data[user_input - 1]
  print(f"You selected: {selected_data['url']}")
  # Return the selected data and its index
  return selected_data, user_input - 1


def load_json_by_number(file_path, number):
  """
  Load a JSON object from a list based on the given number.

  :param file_path: Path to the JSON file.
  :param number: The number corresponding to the index of the JSON object to load.
  :return: The JSON object at the specified index, or None if the index is out of range.
  """
  # Read the existing data from the JSON file
  existing_data = read_json(file_path)
  
  # Check if the number is within the valid range
  if 1 <= number <= len(existing_data):
      # Return the JSON object at the specified index (adjusting for zero-based index)
      return existing_data[number - 1]
  else:
      print(f"Error: Number {number} is out of range. Please select a number between 1 and {len(existing_data)}.")
      return None


def main():
  # Set up argument parser with a description of the script
  parser = argparse.ArgumentParser(description="Mirror Debian like repositories.")
  
  # Create a mutually exclusive group
  group = parser.add_mutually_exclusive_group()
  
  # Define mutually exclusive command-line arguments
  group.add_argument("--add", action='store_true', help="Add repositories in the database")
  group.add_argument("--del", action='store_true', help="Remove repositories in the database")
  group.add_argument("--edit", action='store_true', help="Edit repositories in the database")
  group.add_argument("--list", action='store_true', help="show repositories in the database")
  group.add_argument("--run", action='store_true', help="Run the repositories mirroring")
  
  # Define other command-line arguments
  parser.add_argument("--verbose", action='store_true', help="Verbose mode")
  parser.add_argument("--version", action='version', version="%(prog)s {VERSION}")
  
  try:
      # Parse the command-line arguments
      args = parser.parse_args()
  except SystemExit as e:
      # Handle missing or invalid arguments
      print("Error: Missing or invalid arguments.")
      parser.print_help()
      return
  
  Logger.setup_logging(args.verbose)
  
  if args.add :
    add_data(file_path)

  if args.list:
    list_data(file_path)
 
  if args.edit:
    # Get the selected data from the list_url function
    selected_data, index_data = list_url(file_path)
    selected_data = collect_data(selected_data)
  
    if selected_data is not None:
        logging.debug(f"Loaded JSON object: {selected_data} at index {index_data}")

if __name__ == "__main__":
  main()