
import os
import gnupg
from getpass import getpass
from tkinter import filedialog, Tk
import hashlib

# Définition des répertoires de travail
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TO_ENCRYPT_DIR = os.path.join(BASE_DIR, "ToEncrypt")
ENCRYPTED_DIR = os.path.join(BASE_DIR, "Encrypted")

# Création des dossiers s'ils n'existent pas
for folder in [TO_ENCRYPT_DIR, ENCRYPTED_DIR]:
    os.makedirs(folder, exist_ok=True)

# Initialisation de GPG avec un répertoire dédié pour stocker les clés
GPG_HOME = os.path.join(BASE_DIR, "gnupg")
os.makedirs(GPG_HOME, exist_ok=True)
gpg = gnupg.GPG(gnupghome=GPG_HOME, gpgbinary="/usr/bin/gpg", use_agent=False)

# Fonction de calcul du hash SHA-256 d’un fichier
def calculer_hash(fichier_path):
    h = hashlib.sha256()
    with open(fichier_path, 'rb') as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()

# Création d’un nouveau message texte à chiffrer
def create_message_file():
    print("\n--- Étape 1 : Création d’un nouveau message ---")
    try:
        content = input("Saisis ton message (sur une seule ligne) : ")
        filename = input("Nom du fichier à générer (ex: message.txt) : ")
        file_path = os.path.join(TO_ENCRYPT_DIR, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fichier texte créé avec succès : {file_path}")
        return filename
    except UnicodeDecodeError:
        print("Erreur de saisie : caractères non valides.")
        return None


# Sélection d’un fichier déjà existant dans le dossier ToEncrypt
def select_existing_file():
    print("\n--- Étape 1 : Sélection d’un fichier existant à chiffrer ---")
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir=TO_ENCRYPT_DIR, title="Choisissez un fichier")
    if not file_path:
        print("Aucun fichier sélectionné.")
        return None
    print(f"Fichier sélectionné : {file_path}")
    return file_path

# Génération du hash SHA-256 du fichier et enregistrement dans le dossier Encrypted
def generer_hash(file_path):
    hash_val = calculer_hash(file_path)
    hash_filename = os.path.basename(file_path) + ".hash"
    hash_path = os.path.join(ENCRYPTED_DIR, hash_filename)
    with open(hash_path, "w") as f:
        f.write(hash_val)
    print(f"Hash SHA-256 généré et enregistré dans : {hash_path}")

# Signature numérique du fichier avec la clé privée de l’émetteur
def sign_file(file_path, signer_fingerprint, passphrase):
    print("\n--- Étape 2 : Signature numérique du fichier ---")
    filename = os.path.basename(file_path)
    sig_path = os.path.join(ENCRYPTED_DIR, f"{filename}.sig")
    with open(file_path, "rb") as f:
        signed = gpg.sign_file(
            f,
            keyid=signer_fingerprint,
            detach=True,
            output=sig_path,
            passphrase=passphrase
        )
    if signed:
        print(f"Fichier signé avec succès. Signature enregistrée dans : {sig_path}")
    else:
        print("Erreur lors de la signature :", signed.stderr)

# Chiffrement du fichier avec la clé publique du destinataire
def encrypt_file(file_path, recipient_fingerprint):
    print("\n--- Étape 3 : Chiffrement du fichier ---")
    filename = os.path.basename(file_path)
    output_path = os.path.join(ENCRYPTED_DIR, f"{filename}.gpg")
    with open(file_path, "rb") as f:
        encrypted = gpg.encrypt_file(
            f,
            recipients=[recipient_fingerprint],
            output=output_path,
            always_trust=True
        )
    if encrypted.ok:
        print(f"Fichier chiffré enregistré avec succès : {output_path}")
    else:
        print("Erreur lors du chiffrement :", encrypted.stderr)

# Menu principal de l’émetteur
def main():
    print("\n--- Menu de l'émetteur ---")
    print("1 - Créer un nouveau message à chiffrer")
    print("2 - Sélectionner un fichier existant déjà prêt")

    choix = input("Votre choix : ")

    if choix == "1":
        filename = create_message_file()
        file_path = os.path.join(TO_ENCRYPT_DIR, filename)
    elif choix == "2":
        file_path = select_existing_file()
        if not file_path:
            return
    else:
        print("Choix invalide.")
        return

    print("\n--- Étape 4 : Informations de sécurité ---")
    signer_fingerprint = input("Empreinte de votre clé privée (pour signer) : ")
    passphrase = getpass("Entrez votre passphrase GPG (pour signer) : ")

    print("\n--- Étape 5 : Cible du chiffrement ---")
    recipient_fingerprint = input("Empreinte du destinataire (clé publique) : ")

    # Étapes de traitement
    generer_hash(file_path)
    sign_file(file_path, signer_fingerprint, passphrase)
    encrypt_file(file_path, recipient_fingerprint)

if __name__ == "__main__":
    main()
