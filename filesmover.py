import os
import shutil


def get_folder_path():
    folder_path = input("Enter folder path: ")

    if not os.path.exists(folder_path):
        print("Folder not found.")
        return
    
    return folder_path


def get_destination_folder(filename):
    extension = os.path.splitext(filename)[1].lower()

    if extension == ".pdf":
        return "PDFs"

    elif extension in (".docx", ".txt", ".pptx", ".xlsx"):
        return "Documents"

    elif extension in (".jpg", ".jpeg", ".png"):
        return "Images"

    elif extension in (".mp4", ".mkv", ".avi"):
        return "Videos"

    elif extension in (".mp3", ".wav"):
        return "Music"

    elif extension in (".py", ".cpp", ".java", ".js"):
        return "Code"

    elif extension in (".zip", ".rar", ".7z"):
        return "Archives"
    
    else:
        return "Others"

    

def move_file(folder_path, filename, destination):
    source = os.path.join(folder_path, filename)

    destination_folder = os.path.join(folder_path, destination)

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    destination_path = os.path.join(destination_folder, filename)

    try:
        shutil.move(source, destination_path)

    except Exception as e:
        print(f"Couldn't move {filename}: {e}")

def organize_folder(folder_path):
    files = os.listdir(folder_path)

    for filename in files:
        source = os.path.join(folder_path, filename)

        if os.path.isfile(source):
            destination = get_destination_folder(filename)
            move_file(folder_path, filename, destination)
            print(f"Moved {filename} -> {destination}")


def main():
    folder_path = get_folder_path()

    if folder_path is None:
        return
    
    organize_folder(folder_path)
    print("Finished organizing!")


if __name__ == "__main__":
    main()