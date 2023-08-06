#!/usr/bin/env python3

"""
|============================|
| Desinstalle l'application. |
|============================|

Ce fichier est a la fois un module est un script.

1) Retire raisin des applications au demarrage.
2) Supprime les repertoires crees par raisin.
3) Supprime les raccourcis qui pointent vers raisin.
"""

import os
import re
import shutil

import raisin.tools as tools # On ne fait pas d'import relatif
import raisin.application.settings as settings # de facon a ce qu'on
import raisin.application.hmi.dialog as dialog # puisse l'excecuter directement.


def uninstall_startup(home):
    """
    |====================================|
    | Supprime le demarrage automatique. |
    |====================================|

    Desamorce si possible la partie de raisin
    qui se lance toute seule.

    entree
    ------
    :param home: Le chemin de l'utilisateur
        concerne par le desamorcage.
        Ou la valeur speciale: 'all_users'.
    :type home: str
    """
    assert isinstance(home, str), \
        "'home' doit etre de type str, pas %s." \
        % type(home).__name__
    assert home == "all_users" or os.path.isdir(home), \
        "%s n'est pas un repertoire existant." % repr(home)

    with tools.Printer(
            "Removing raisin to apps at startup for {}...".format(
            "'root'" if home == "all_users" else repr(os.path.basename(home)))) as p:
        if os.name == "posix":
            if home == "all_users":
                if os.system("systemctl stop raisin.service"):
                    p.show("Failed to stop the 'raisin' service.")
                else:
                    p.show("The 'raisin' service is stoped.")
                if os.system("systemctl disable raisin.service"):
                    p.show("Failed to disable the 'raisin' service.")
                else:
                    p.show("The 'raisin' service is disabled.")
                path = "/lib/systemd/system/raisin.service"
                if os.path.exists(path):
                    os.remove(path)
                    p.show("Removed %s." % repr(path))
                else:
                    p.show("Failed removed %s." % repr(path))
            else:
                if os.system("systemctl --user stop raisin.service"):
                    p.show("Failed to stop the 'raisin' service.")
                else:
                    p.show("The 'raisin' service is stoped.")
                if os.system("systemctl --user disable raisin.service"):
                    p.show("Failed to disable the 'raisin' service.")
                else:
                    p.show("The 'raisin' service is disabled.")
                path = os.path.join(home, ".config/systemd/user/raisin.service")
                if os.path.exists(path):
                    os.remove(path)
                    p.show("Removed %s." % repr(path))
                else:
                    p.show("Failed removed %s." % repr(path))
        elif os.name == "nt":
            if home == "all_users":
                if os.path.exists("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\"
                        "Programs\\Startup\\raisin.pyw"):
                    os.remove("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\"
                        "Programs\\Startup\\raisin.pyw")
                    p.show("The 'raisin.pyw' file is deleted.")
                else:
                    p.show("Failed to delete the 'raisin.pyw' file.")
            else:
                if os.path.exists(os.path.join(home, "AppData\\Roaming\\Microsoft\\"
                        "Windows\\Start Menu\\Programs\\Startup\\raisin.pyw")):
                    os.remove(os.path.join(home, "AppData\\Roaming\\Microsoft\\" \
                        "Windows\\Start Menu\\Programs\\Startup\\raisin.pyw"))
                    p.show("The 'raisin.pyw' file is deleted.")
                else:
                    p.show("Failed to delete the 'raisin.pyw' file.")

def uninstall_settings(home):
    """
    |================================|
    | Mange les crottes de 'raisin'. |
    |================================|

    * Supprime le repertoire '.raisin'.
    * Supprime aussi le repertoire d'enregistrement des resultats
        si il existe.

    entree
    ------
    :param home: Le chemin de l'utilisateur
        concerne par le desamorcage.
        Ou la valeur speciale: 'all_users'.
    :type home: str
    """
    assert isinstance(home, str), \
        "'home' doit etre de type str, pas %s." \
        % type(home).__name__
    assert home == "all_users" or os.path.isdir(home), \
        "%s n'est pas un repertoire existant." % repr(home)

    with tools.Printer(
            "Uninstall settings for {}...".format(
            "'root'" if home == "all_users" else repr(os.path.basename(home)))) as p:
        
        # Suppression rep enregistrement.
        real_home = os.path.expanduser("~") if home == "all_users" else home
        recording_directory = settings.Settings(home=real_home)["cluster_work"]["recording_directory"]
        if os.path.exists(recording_directory):
            shutil.rmtree(recording_directory)
            p.show("Removed %s." % repr(recording_directory))
        
        # Suppression rep de base.
        raisin_path = os.path.join(home, ".raisin")
        if os.path.exists(raisin_path):
            shutil.rmtree(raisin_path)
            p.show("Removed %s." % repr(raisin_path))
        else:
            p.show("Rep not found %s." % repr(raisin_path))

def uninstall_shortcut(home):
    """
    |=====================|
    | Supprime les alias. |
    |=====================|
    
    entree
    ------
    :param home: Le chemin de l'utilisateur
        concerne par le desamorcage.
        Ou la valeur speciale: 'all_users'.
    :type home: str
    """
    assert isinstance(home, str), \
        "'home' doit etre de type str, pas %s." \
        % type(home).__name__
    assert home == "all_users" or os.path.isdir(home), \
        "%s n'est pas un repertoire existant." % repr(home)

    with tools.Printer(
            "Uninstall shortcut for {}...".format(
            "'root'" if home == "all_users" else repr(os.path.basename(home)))) as p:
       
        real_home = os.path.expanduser("~") if home == "all_users" else home
        
        if os.name == "posix":
            bashrc = os.path.join(real_home, ".bashrc")
            with open(bashrc, "r", encoding="utf-8") as f:
                lines = [l for l in f if not re.search(r"alias raisin='.+ -m raisin'", l)]
                while lines and lines[-1] == "\n":
                    del lines[-1]
            with open(bashrc, "w", encoding="utf-8") as f:
                f.write("".join(lines))
            p.show("Removed raisin from %s." % repr(bashrc))
            # os.system("source ~/.bashrc") # Pour endre effectif.

        elif os.name == "nt":
            profile = os.path.join(real_home, "Documents", "profile.ps1")
            if os.path.exists(profile):
                with open(profile, "r", encoding="utf-8") as f:
                    lines = [l for l in f if not re.search(r"Set-Alias raisin '.+ -m raisin'", l)]
                    while lines and lines[-1] == "\n":
                        del lines[-1]
                if lines:
                    with open(profile, "w", encoding="utf-8") as f:
                        f.write("".join(lines))
                    p.show("Removed raisin from the 'profile.ps1' file")
                else:
                    os.remove(profile)
                    p.show("Removed %s." % repr(profile))
            else:
                p.show("File not found %s." % repr(profile))

def _list_home():
    """
    |===================================|
    | Liste les utilisateurs concernes. |
    |===================================|

    * Cede les repertoires personels de
    tous les utilisateurs qui doivent
    beneficier de la desinstallation de raisin.
    * Si cette fonction est lancee avec les
    droits administrateurs et que l'utilisateur
    veut faire que plus personne n'ai raisin,
    retourne la valeur speciale: 'all_users'.

    sortie
    ------
    :return: Le chemin du repertoire personel
        de chaque utilisateur concerne. Ou
        la valeur speciale: 'all_users'.
    :rtype: str
    """
    if tools.identity["has_admin"]:
        if 0 == dialog.question_choix_exclusif(
                question="How do you want to uninstall 'raisin'?",
                choix=["Do you want uninstall 'raisin' for each user?",
                       "Do you want uninstall 'raisin' for 'root'?"]):
            racine = "C:\\Users" if os.name == "nt" else "/home"
            for user in os.listdir(racine):
                yield os.path.join(racine, user)
        else:
            yield "all_users"
    else:
        yield os.path.expanduser("~")

def main():
    """
    Desinstalle entierement l'application raisin.
    """
    with tools.Printer("Uninstall raisin..."):
        for home in _list_home():
            uninstall_shortcut(home)
            uninstall_settings(home)
            uninstall_startup(home)

if __name__ == "__main__":
    main()
