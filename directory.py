import os

def create_project_directories():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folders = ["ToEncrypt", "Encrypted", "Decrypted", "Imported", "gnupg"]

    for folder in folders:
        path = os.path.join(base_dir, folder)
        os.makedirs(path, exist_ok=True)
        print(f"Dossier créé (ou déjà existant) : {path}")

if __name__ == "__main__":
    create_project_directories()
