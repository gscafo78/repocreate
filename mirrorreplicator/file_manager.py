import os

class FileManager:
  @staticmethod
  def list_files_recursive(folder_path):
      file_list = []
      for root, _, files in os.walk(folder_path):
          for file in files:
              file_list.append(os.path.join(root, file))
      return file_list

  @staticmethod
  def list_files_in_folder(folder_path):
      try:
          files = os.listdir(folder_path)
          file_paths = [os.path.join(folder_path, f) for f in files if os.path.isfile(os.path.join(folder_path, f))]
          return file_paths
      except Exception as e:
          print(f"An error occurred: {e}")
          return []

  @staticmethod
  def delete_files(file_list):
      for file_path in file_list:
          try:
              os.remove(file_path)
              print(f"Deleted: {file_path}")
          except FileNotFoundError:
              print(f"File not found: {file_path}")
          except PermissionError:
              print(f"Permission denied: {file_path}")
          except Exception as e:
              print(f"Error deleting {file_path}: {e}")