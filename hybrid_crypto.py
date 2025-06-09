
import os
import gnupg
from getpass import getpass
from tkinter import Tk, filedialog

# Répertoires de travail
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TO_ENCRYPT_DIR = os.path.join(BASE_DIR, "ToEncrypt")
ENCRYPTED_DIR = os.path.join(BASE_DIR, "Encrypted")
DECRYPTED_DIR = os.path.join(BASE_DIR, "Decrypted")

# Création des dossiers s’ils n’existent pas
for folder in [TO_ENCRYPT_DIR, ENCRYPTED_DIR, DECRYPTED_DIR]:
    os.makedirs(folder, exist_ok=True)

# Initialisation GPG
GPG_HOME = os.path.join(BASE_DIR, "gnupg")
os.makedirs(GPG_HOME, exist_ok=True)
gpg = gnupg.GPG(gnupghome=GPG_HOME, gpgbinary="/usr/bin/gpg")

# ======================== GÉNÉRATION DE CLÉ ========================
def generate_key():
    print("\n--- Génération d'une paire de clés GPG ---")
    print("Cette clé servira à signer ou déchiffrer des messages.")
    name = input("Votre nom complet : ")
    email = input("Votre adresse email : ")
    passphrase = getpass("Définissez une passphrase (mot de passe) : ")

    input_data = gpg.gen_key_input(name_real=name, name_email=email, passphrase=passphrase)
    key = gpg.gen_key(input_data)

    if key:
        print("Clé générée avec succès.")
        print("Empreinte à conserver :", key.fingerprint)
    else:
        print("Erreur lors de la génération de la clé.")

# ======================== LISTE DES CLÉS ========================
def list_keys():
    print("\n--- Liste des clés GPG publiques ---")
    print("Voici les clés que vous possédez dans votre trousseau :\n")
    keys = gpg.list_keys()
    if not keys:
        print("Aucune clé trouvée.")
    for i, key in enumerate(keys):
        print(f"{i+1}. {key['uids'][0]} - {key['fingerprint']}")

# ======================== ENVOI VERS SERVEUR ========================
def send_key_to_server():
    print("\n--- Envoi d'une clé publique vers un serveur de clés ---")
    print("Cela permet à d'autres de retrouver votre clé publique.")
    fingerprint = input("Entrez l'empreinte de la clé à publier : ")
    result = gpg.send_keys('keyserver.ubuntu.com', fingerprint)
    print("Résultat :", result)

# ======================== IMPORTATION DE CLÉ ========================
def import_key_from_file():
    print("\n--- Importation d'une clé publique à partir d'un fichier .asc ---")
    print("Cette opération ajoute une clé publique reçue dans votre trousseau local.")
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        initialdir=os.path.join(BASE_DIR, "Imported"),
        title="Sélectionnez la clé publique à importer (.asc)",
        filetypes=[("Fichiers ASCII GPG", "*.asc")]
    )
    root.destroy()

    if file_path:
        with open(file_path, "r") as f:
            result = gpg.import_keys(f.read())
        if result.count > 0:
            print("Clé importée avec succès.")
            for k in result.fingerprints:
                print("Empreinte de la clé :", k)
        else:
            print("Échec de l'importation de la clé.")
    else:
        print("Aucun fichier sélectionné.")

# ======================== SUPPRESSION DE CLÉ ========================
def delete_key():
    print("\n--- Suppression d'une clé ---")
    print("Attention : cette opération est irréversible.")
    list_keys()
    fingerprint = input("\nEntrez l'empreinte de la clé à supprimer : ").strip()
    confirm = input("Confirmez-vous la suppression ? (o/n) : ").strip().lower()

    if confirm != 'o':
        print("Suppression annulée.")
        return

    pub_keys = gpg.list_keys()
    priv_keys = gpg.list_keys(secret=True)

    pub_present = any(key['fingerprint'] == fingerprint for key in pub_keys)
    priv_present = any(key['fingerprint'] == fingerprint for key in priv_keys)

    if not pub_present and not priv_present:
        print("Erreur : aucune clé correspondant à cette empreinte n’a été trouvée dans le trousseau GPG local.")
        return

    if priv_present:
        passphrase = getpass("Entrez la passphrase de la clé secrète : ")
        try:
            result_sec = gpg.delete_keys(fingerprint, secret=True, passphrase=passphrase)
            print("Clé privée supprimée :", result_sec.status)
        except ValueError as e:
            print("Erreur lors de la suppression de la clé privée :", str(e))
    else:
        print("Aucune clé privée à supprimer.")

    if pub_present:
        result_pub = gpg.delete_keys(fingerprint)
        print("Clé publique supprimée :", result_pub.status)
    else:
        print("Aucune clé publique à supprimer.")

# ======================== MENU PRINCIPAL ========================
def main():
    while True:
        print("\n========= MENU CRYPTOGRAPHIE =========")
        print("1. Générer une nouvelle paire de clés")
        print("2. Lister les clés de votre trousseau")
        print("3. Envoyer une clé publique au serveur de clés")
        print("4. Importer une clé depuis un fichier (.asc)")
        print("5. Supprimer une clé")
        print("0. Quitter")
        print("======================================")

        choix = input("Votre choix : ").strip()
        if choix == "1":
            generate_key()
        elif choix == "2":
            list_keys()
        elif choix == "3":
            send_key_to_server()
        elif choix == "4":
            import_key_from_file()
        elif choix == "5":
            delete_key()
        elif choix == "0":
            print("Fin du programme. À bientôt.")
            break
        else:
            print("Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
