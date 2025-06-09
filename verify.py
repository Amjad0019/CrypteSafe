import gnupg
import os
import hashlib
from tkinter import Tk, filedialog

# Répertoires principaux de CrypteSafe
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GPG_DIR = os.path.join(BASE_DIR, "gnupg")
DECRYPTED_DIR = os.path.join(BASE_DIR, "Decrypted")
IMPORTED_DIR = os.path.join(BASE_DIR, "Imported")

# Création des répertoires si nécessaires
os.makedirs(GPG_DIR, exist_ok=True)
os.makedirs(DECRYPTED_DIR, exist_ok=True)
os.makedirs(IMPORTED_DIR, exist_ok=True)

# Initialisation de GPG
gpg = gnupg.GPG(gnupghome=GPG_DIR, gpgbinary="/usr/bin/gpg")

def select_file(title, filetypes, initial_folder):
    """
    Ouvre une boîte de dialogue pour sélectionner un fichier à un emplacement spécifique.
    """
    print(f"\n{title}")
    root = Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title=title,
        filetypes=filetypes,
        initialdir=initial_folder
    )
    root.destroy()
    return path

def compute_sha256(file_path):
    """
    Calcule le hash SHA-256 d’un fichier donné.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()

def verify_signature_and_integrity():
    print("\n=== VÉRIFICATION DE LA SIGNATURE ET DE L'INTÉGRITÉ D'UN FICHIER ===")

    # Étape 1 : Sélection du fichier de signature
    sig_path = select_file("Étape 1 : Sélectionnez le fichier .sig", [("Fichiers .sig", "*.sig")], IMPORTED_DIR)
    if not sig_path:
        print("Aucun fichier de signature sélectionné.")
        return

    # Étape 2 : Sélection du fichier déchiffré
    decrypted_path = select_file("Étape 2 : Sélectionnez le fichier déchiffré (.decrypted)", [("Fichiers déchiffrés", "*.decrypted")], DECRYPTED_DIR)
    if not decrypted_path:
        print("Aucun fichier déchiffré sélectionné.")
        return

    # Étape 3 : Sélection du fichier de hash
    hash_path = select_file("Étape 3 : Sélectionnez le fichier .hash", [("Fichiers .hash", "*.hash")], IMPORTED_DIR)
    if not hash_path:
        print("Aucun fichier de hash sélectionné.")
        return

    # Vérification de la signature
    print("\n--- Vérification de la signature ---")
    with open(decrypted_path, "rb") as f, open(sig_path, "rb") as s:
        verified = gpg.verify_file(s, f.name)

    if verified:
        print("Signature VALIDE.")
        print("Fichier signé par :", verified.username or "Inconnu")
        print("Empreinte du signataire :", verified.fingerprint or "Non disponible")
    else:
        print("Signature NON VALIDE ou échec de vérification.")
        return

    # Vérification de l'intégrité
    print("\n--- Vérification de l'intégrité SHA-256 ---")
    with open(hash_path, "r") as f:
        expected_hash = f.read().strip()

    current_hash = compute_sha256(decrypted_path)

    print("Hash attendu :", expected_hash)
    print("Hash actuel  :", current_hash)

    if current_hash == expected_hash:
        print("Intégrité confirmée : le fichier n’a pas été modifié.")
    else:
        print("Intégrité compromise : le fichier a été altéré ou corrompu.")

def main():
    verify_signature_and_integrity()

if __name__ == "__main__":
    main()
