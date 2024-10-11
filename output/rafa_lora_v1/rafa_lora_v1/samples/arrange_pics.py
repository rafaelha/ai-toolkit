import os
import shutil

def move_files_based_on_last_digit(source_folder):
    # Get a list of all files in the directory
    files = os.listdir(source_folder)
    
    # Loop through each file
    for file in files:
        if file.endswith(".jpg"):
            # Extract the last digit before the extension
            last_digit = file.split("_")[-1].split(".")[0]
            
            # Create the destination folder if it doesn't exist
            destination_folder = os.path.join(source_folder, last_digit)
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            
            # Move the file to the appropriate folder
            src_file_path = os.path.join(source_folder, file)
            dest_file_path = os.path.join(destination_folder, file)
            shutil.move(src_file_path, dest_file_path)
            
    print("Files moved successfully!")

# Specify the path where your files are located
source_folder = "."  # Replace with the actual path
move_files_based_on_last_digit(source_folder)

#%%
# import os
# import shutil

# def redo_move_files_based_on_last_digit(source_folder):
#     # Get a list of all directories in the source folder
#     directories = [d for d in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, d))]
    
#     # Loop through each directory
#     for directory in directories:
#         dir_path = os.path.join(source_folder, directory)
        
#         # Get a list of all files in the directory
#         files = os.listdir(dir_path)
        
#         # Move each file back to the source folder
#         for file in files:
#             src_file_path = os.path.join(dir_path, file)
#             dest_file_path = os.path.join(source_folder, file)
#             shutil.move(src_file_path, dest_file_path)
        
#         # Remove the now-empty directory
#         os.rmdir(dir_path)
    
#     print("Files moved back successfully!")

# # Specify the path where your files are located
# source_folder = "."  # Replace with the actual path
# redo_move_files_based_on_last_digit(source_folder)