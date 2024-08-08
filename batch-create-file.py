import os

def create_files(path,filename):
# path = "D:\Projects\\repos\\python-small-apps\\translator"

    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a valid directory")
        return
    
    for dir in os.listdir(path):
        if os.path.isdir(dir):
            file_path = os.path.join(path,dir,filename)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write(f"# {dir}")

    print("All files created!")

if __name__ == "__main__":
    path = input("Enter path to rootdir: ")
    filename = input("Enter name of files to create: ")
    create_files(path,filename)