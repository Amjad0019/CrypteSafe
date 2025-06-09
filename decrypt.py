import gnupg
import os
from tkinter import Tk, filedialog
from getpass import getpass

# Configuration du répertoire GPG
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GPG_DIR = os.path.join(BASE_DIR, "gnupg")
os.makedirs(GPG_DIR, exist_ok=True)

# Initialisation de GPG
gpg = gnupg.GPG(gnupghome=GPG_DIR, gpgbinary="/usr/bin/gpg")

# Répertoire de sortie avec "/home/falihi/CrypteSafe/Imported" à modifier
DECRYPTED_DIR = os.path.join(BASE_DIR, "Decrypted")
os.makedirs(DECRYPTED_DIR, exist_ok=True)

def select_file(title, filetypes):
    print("Veuillez sélectionner le fichier via la fenêtre qui s’ouvre.")
    root = Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title=title,
        filetypes=filetypes,
        initialdir="/home/falihi/CrypteSafe/Imported"
    )
    root.destroy()
    return path

def decrypt_file():
    print("\n--- Étape 1 : Déchiffrement d’un fichier ---")
    encrypted_path = select_file("Sélectionner le fichier .gpg à déchiffrer", [("Fichiers GPG", "*.gpg")])
    if not encrypted_path:
        print("Aucun fichier sélectionné. Annulation du processus.")
        return

    fingerprint = input("Entrez l'empreinte de votre clé privée : ")
    passphrase = getpass("Entrez votre passphrase GPG : ")

    output_file = os.path.join(DECRYPTED_DIR, os.path.basename(encrypted_path).replace(".gpg", ".decrypted"))

    print("Déchiffrement en cours...")
    with open(encrypted_path, "rb") as ef:
        decrypted = gpg.decrypt_file(ef, passphrase=passphrase, output=output_file)

    if decrypted.ok:
        print(f"Fichier déchiffré avec succès. Chemin : {output_file}")
        print("Vous pouvez maintenant ouvrir ce fichier manuellement.")
    else:
        print("Erreur de déchiffrement :", decrypted.stderr)

def main():
    print("\n=== DÉCHIFFREMENT D’UN FICHIER SÉCURISÉ ===")
    decrypt_file()

if __name__ == "__main__":
    main()
