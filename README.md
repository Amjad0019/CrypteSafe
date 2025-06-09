# CrypteSafe

## Documentation Utilisateur & Technique

### Objectif du projet

CrypteSafe est une application locale permettant de **chiffrer**, **déchiffrer**, **signer** et **vérifier l'intégrité** des fichiers à l'aide de la **cryptographie hybride** (AES + RSA) et de **GnuPG**.

Ce projet s'adresse à toute personne souhaitant échanger des fichiers de manière **confidentielle, intègre et authentique**, sans passer par une plateforme tierce.

---

## Prérequis & Installation

### 1. Installer les outils système (Linux / WSL Ubuntu)

```bash
sudo apt update && sudo apt install python3 python3-pip gnupg python3-tk
```

### 2. Créer et activer un environnement virtuel Python

```bash
cd ~/CrypteSafe  # se placer dans le dossier du projet
python3 -m venv venv  # création
source venv/bin/activate  # activation (Linux/Mac)
```

> Pour Windows avec PowerShell :

```powershell
venv\Scripts\activate
```

### 3. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

---

## Arborescence des dossiers

```bash
CrypteSafe/
|
├── ToEncrypt/        # Dossiers contenant les fichiers à chiffrer
├── Encrypted/        # Fichiers chiffrés, signés et hashés
├── Decrypted/        # Fichiers déchiffrés
├── Imported/         # Clés et fichiers reçus
├── gnupg/            # Trousseau local de GPG (clés)
├── venv/             # Environnement virtuel Python
├── hybrid_crypto.py  # Script de gestion des clés
├── encrypt.py        # Chiffrement et signature
├── decrypt.py        # Déchiffrement
├── verify.py         # Vérification signature et intégrité
└── directory.py      # Génération des dossiers
```

---

## Utilisation des scripts

### 1. Gérer les clés GPG : `hybrid_crypto.py`

```bash
python hybrid_crypto.py
```

Ce menu propose :

* Générer une paire de clés
* Lister les clés
* Envoyer une clé publique
* Importer une clé publique depuis un fichier
* Supprimer une clé

### 2. Chiffrer un fichier : `encrypt.py`

```bash
python encrypt.py
```

* Permet de créer un fichier ou d’en sélectionner un depuis `ToEncrypt/`
* Signature via la clé privée
* Chiffrement avec la clé publique du destinataire
* Génère 3 fichiers : `.gpg`, `.sig`, `.hash`

### 3. Déchiffrer un fichier : `decrypt.py`

```bash
python decrypt.py
```

* Sélection du fichier `.gpg` dans `Imported/`
* Requiert l’empreinte de la clé privée et la passphrase
* Dépose le fichier `.decrypted` dans `Decrypted/`

### 4. Vérifier signature et intégrité : `verify.py`

```bash
python verify.py
```

* Sélectionner : `.sig`, `.decrypted`, `.hash`
* Affiche : validité de la signature, auteur et empreinte, vérification de l’intégrité SHA-256

---

## Bonnes pratiques

* Toujours vérifier la signature et le hash avant d’ouvrir un fichier déchiffré
* Ne jamais transmettre sa clé privée
* Exporter sa clé publique pour la transmettre sécurisément
* Supprimer une clé uniquement si elle n’est plus utilisée

---

## Partage manuel de clés publiques

Le script n'intègre pas de recherche automatique en ligne (volonté de contrôle et transparence).

Pour importer une clé publique :

1. Rendez-vous sur : [https://keyserver.ubuntu.com](https://keyserver.ubuntu.com)
2. Recherchez l'adresse email du destinataire
3. Téléchargez sa clé publique (.asc)
4. Placez-la dans le dossier `Imported/`
5. Lancez `hybrid_crypto.py` > Importer une clé depuis un fichier

---

## Conclusion

Ce guide permet de prendre en main CrypteSafe pas à pas, même pour un utilisateur n'ayant aucune expérience préalable du terminal ou de la cryptographie. L’objectif est de rendre l’autonomie accessible, sans compromettre la sécurité.

Pour toute contribution ou amélioration, vous pouvez créer une **pull request** sur le dépôt GitHub associé.

