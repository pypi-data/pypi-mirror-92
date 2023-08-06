#!/usr/bin/env python3

"""
|=========================|
| Installe l'application. |
|=========================|

Ce fichier est a la fois un module est un script.

1) Gives write rights to the 'grape' module folder so as to allow updates.
2) Append alias/shortcut for 'raisin' command line.
3) Creation and recording of 'rasin' parameters.
4) Ensures that 'raisin' starts up on its own at the start.
"""

import os
import sys

import raisin.tools as tools # On ne fait pas d'import relatif
import raisin.application.hmi.dialog as dialog # afin de pouvoir le faire
import raisin.application.module as module # fonctionner comme un script.
import raisin.application.uninstall as uninstall
import raisin.application.upgrade as upgrade
import raisin.application.settings as settings


def install_dependencies():
    """
    Recherche les dependances non satisfaites de raisin
    et tente de les installer si l'utilisateur est d'accord.
    """
    # global tkinter, ttk # evite l'erreur: UnboundLocalError: local variable 'tkinter' referenced before assignment

    dependencies = module.get_unmet_dependencies("raisin") # recherches des dependances non satisfaites de raisin
    if dependencies:
        if dialog.question_binaire(
                "'raisin' depend des modules suivants:\n" \
                + " %s\n" % ", ".join(dependencies) \
                + "Voulez-vous les installer?", default=True):
            if not tools.identity["has_admin"]:
                if dialog.question_binaire(
                        "Vous n'avez pas les droits administrateur.\n"
                        "Preferez-vous installer les modules en tant "
                        "qu'administrateur?", default=True):
                    command = '%s -c "\n' % sys.executable
                    command += 'from raisin.application import module\n' \
                            + 'for dep in %s:\n' % repr(dependencies) \
                            + '\tmodule.install(dep)\n' \
                            + '"'
                    if os.name == "nt":
                        sudo = "runas /user:%s\\administrator" \
                                % tools.identity["hostname"]
                    else:
                        sudo = "sudo"
                    sudo_command = sudo + " " + command
                    with tools.Printer(
                        "Install dependencies as administrator...") as p:
                        p.show("$ %s" % repr(sudo_command))
                        os.system(sudo_command)
                    return
                else:
                    message = "Install dependencies without administrator rights..."
            else:
                message = "Install dependencies with administrator rights..."
            with tools.Printer(message):
                for dep in dependencies:
                    module.install(dep)

def install_shortcut(home):
    """
    |============================================|
    | Ajoute des alias qui pointent vers raisin. |
    |============================================|

    Se contente de faire l'alias permanent suivant:
    'python3 -m raisin' devient simplement 'raisin'

    entree
    ------
    :param home: Le chemin de l'utilisateur
        concerne par l'installation.
        Ou la valeur speciale: 'all_users'.
    :type home: str
    """
    assert isinstance(home, str), \
        "'home' have to be str, not %s." % type(home).__name__
    assert home == "all_users" or os.path.isdir(home), \
        "'home' have to be a repository. " \
        + "%s is not an existing repository." % repr(home)

    with tools.Printer(
            "Install shortcut for {}...".format(
            "'root'" if home == "all_users" else repr(os.path.basename(home)))):
        uninstall.uninstall_shortcut(home) # On prend des precautions
        real_home = os.path.expanduser("~") if home == "all_users" else home
        if os.name == "posix":
            config_file = os.path.join(real_home, ".bashrc")
            command = "alias raisin='%s -m raisin'" % sys.executable
            # os.system(". ~/.bashrc") # Pour endre effectif.
        elif os.name == "nt":
            config_file = os.path.join(real_home, "Documents", "profile.ps1")
            command = "Set-Alias raisin '%s -m raisin'" % sys.executable
        
        with open(config_file, "a", encoding="utf-8") as f:
            f.write("\n")
            f.write(command)
            f.write("\n")

def install_settings(home, action):
    """
    |==============================|
    | Genere et enregistres les    |
    | parametres de l'utilisateur. |
    |==============================|

    entree
    ------
    :param home: Le chemin de l'utilisateur
        concerne par l'installation.
        Ou la valeur speciale: 'all_users'.
    :type home: str
    :param action: Le mode d'installation:
        - 'paranoiac' Pour une securitee maximale,
            au detriment parfois de l'efficacite.
        - 'normal' Pour un bon compromis entre la securite,
            la vie privee et l'efficacite.
        - 'altruistic' Pour maximiser l'efficacite,
            au detriment de la securite et de la vie privee.
        - 'custom' Pose la question a l'utilisateur a chaque etape.
    :type action: str
    """
    assert isinstance(home, str), \
        "'home' have to be str, not %s." % type(home).__name__
    assert isinstance(action, str), \
        "'action' have to be str, not %s." % type(action).__name__
    assert home == "all_users" or os.path.isdir(home), \
        "'home' have to be a repository. " \
        + "%s is not an existing repository." % repr(home)
    assert action in ("paranoiac", "normal", "altruistic", "custom"), \
            "Les actions ne peuvent que etre 'paranoiac', " \
            + "'normal', 'altruistic' ou 'custom'. Pas '%s'." % action

    with tools.Printer(
            "Install settings for {}...".format(
            "'root'" if home == "all_users" else repr(os.path.basename(home)))):
        home = os.path.expanduser("~") if home == "all_users" else home
        s = settings.Settings(home=home, action=action)
        s.flush()

def install_startup(home):
    r"""
    |==========================|
    | Fait en sorte que raisin |
    | se lance de lui-meme.    |
    |==========================|

    * Si 'home' vaut "all_users":
        - Fait en sorte que 'raisin' se
        lance une seule fois au
        demmarrage de l'ordinateur.
    * Si 'home' vaut "/home/<username>":
        - Fait en sorte qu'une instance de raisin
        se lance des que le user <username>
        se connecte a sa session.
    * Si 'home' vaut "C:\\Users\\<username>":
        - Fait comme juste au dessus mais ne
        restreind pas les droit de l'application
        car sur windows c'est complique.

    entree
    ------
    :param home: Le chemin de l'utilisateur
        concerne par l'installation.
        Ou la valeur speciale: 'all_users'.
    :type home: str

    sortie
    ------
    :raises PermissionError: Si les droits ne sont pas suffisants
        pour installer les fichiers la ou il faut.
    :raises SystemError: Si le systeme d'exploitation ne permet
        pas a raisin de se debrouiller tout seul.
    :raises FileExistsError: Si raisin est deja installe.
    """
    assert isinstance(home, str), \
        "'home' doit etre de type str, pas %s." \
        % type(home).__name__
    assert home == "all_users" or os.path.isdir(home), \
        "%s n'est pas un repertoire existant." % repr(home)

    INSTRUCTIONS = ["start", "--server", "--upgrade"]
    with tools.Printer(
            "Adding raisin to apps at startup for {}...".format(
            "'root'" if home == "all_users" else repr(os.path.basename(home)))) as p:

        # Recherche de la configuration existante.
        p.show("Finding the current configuration.")
        if os.name == "posix":
            if not os.path.exists("/lib/systemd/system/"):
                raise SystemError("It doesn't appear that "
                    "the service manager is 'systemd'.")
            root_path = os.path.exists("/lib/systemd/system/raisin.service")
            user_path = os.path.exists(os.path.join(
                home, ".config/systemd/user/raisin.service"))
        elif os.name == "nt":
            root_path = os.path.exists("C:\\ProgramData\\Microsoft\\"
                "Windows\\Start Menu\\Programs\\Startup\\raisin.pyw")
            user_path = os.path.exists(os.path.join(
                home, "AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\"
                "Programs\\Startup\\raisin.pyw"))
        else:
            raise SystemError("I don't know the standard %s." % repr(os.name),
                "I can to succeed with 'posix' or 'nt'.")

        # Verification de la coherence.
        p.show("Checking consistency.")
        if home == "all_users" and root_path:
            raise FileExistsError(
                "The raisin service is already runing for all users.")
        elif home != "all_users" and user_path:
            raise FileExistsError(
                "The raisin service is already runing for %s." \
                % repr(os.path.basename(home)))
        elif home != "all_users" and root_path:
            raise FileExistsError("We are not going to do an individual "
                "installation when there is already runing for all users.")
        else: # Si il faut installer en globale, on desinstalle en locale.
            racine = "C:\\Users" if os.name == "nt" else "/home"
            presents = [
                user for user in os.listdir(racine)
                if os.path.exists(os.path.join(racine, user, ".config/systemd/"
                    "user/raisin.service"))
                or os.path.exists(os.path.join(racine, user, "AppData\\Roaming\\"
                    "Microsoft\\Windows\\Start Menu\\Programs\\Startup\\raisin.pyw"))]
            if presents and dialog.question_binaire(
                    question=("'raisin' est deja installe pour %s.\n"
                        % ", ".join(presents) \
                        + "Voulez vous d'abord desinstaller 'raisin' pour " \
                        + "ces utilisateurs avant de le reinstaller pour tous?"),
                    default=True):
                for user in presents:
                    uninstall.uninstall_startup(os.path.join(
                        "C:\\Users" if os.name == "nt" else "/home", user))
            elif presents:
                raise FileExistsError("Before to install 'raisin' for all "
                    "users, you must uninstall 'raisin' for %s." % ", ".join(presents))

        # Preparation des dossiers.
        if os.name == "posix":
            if home != "all_users" and not os.path.exists(os.path.join(
                    home, ".config/systemd/user/")):
                os.makedirs(os.path.join(home, ".config/systemd/user/"))

        # Installation des fichiers.
        if os.name == "posix":
            command = "%s -m raisin %s" % (sys.executable, " ".join(INSTRUCTIONS))
            if home == "all_users":
                p.show("Writing '/lib/systemd/system/raisin.service'.")
                with open("/lib/systemd/system/raisin.service", "w") as f:
                    f.write(
                          "[Unit]\n" \
                        + "Description=The 'raisin' service for all users.\n" \
                        + "After=network-online.target\n" \
                        + "\n" \
                        + "[Service]\n" \
                        + "Type=simple\n" \
                        + "ExecStart=%s\n" % command \
                        + "Restart=on-abort\n" \
                        + "\n" \
                        + "[Install]\n" \
                        + "WantedBy=multi-user.target\n")
                os.chmod("/lib/systemd/system/raisin.service", 0o644)
                if os.system("systemctl enable raisin.service"):
                    raise SystemError("Impossible d'excecuter: 'systemctl enable raisin.service'")
                if os.system("systemctl start raisin.service"):
                    raise SystemError("Impossible d'excecuter: 'systemctl start raisin.service'")
            else:
                p.show("Writing %s." % repr(os.path.join(
                    home, ".config/systemd/user/raisin.service")))
                with open(os.path.join(home, ".config/systemd/user/raisin.service"), "w") as f:
                    f.write(
                          "[Unit]\n" \
                        + "Description=The 'raisin' service for %s.\n" % repr(
                            os.path.basename(home)) \
                        + "After=network-online.target\n" \
                        + "\n" \
                        + "[Service]\n" \
                        + "Type=simple\n" \
                        # + "User=deluge\n" \
                        # + "Group=deluge\n" \
                        + "ExecStart=%s\n" % command \
                        + "Restart=on-failure\n" \
                        + "\n" \
                        + "[Install]\n" \
                        + "WantedBy=default.target\n")
                if os.system("systemctl --user enable raisin.service"):
                    raise SystemError("Impossible d'excecuter: 'systemctl --user enable raisin.service'")
                if os.system("systemctl --user start raisin.service"):
                    raise SystemError("Impossible d'excecuter: 'systemctl --user start raisin.service'")
        elif os.name == "nt":
            if home == "all_users":
                filename = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\" \
                    "Programs\\Startup\\raisin.pyw"
            else:
                filename = os.path.join(home, "AppData\\Roaming\\Microsoft\\" \
                    "Windows\\Start Menu\\Programs\\Startup\\raisin.pyw")
            p.show("Writing %s." % repr(filename))
            with open(filename, "w") as f:
                f.write("import raisin.__main__\n"
                        "\n"
                        "raisin.__main__.main([%s])\n" % ", ".join(INSTRUCTIONS))

def _list_home():
    """
    |===================================|
    | Liste les utilisateurs concernes. |
    |===================================|

    * Cede les repertoires personels de
    tous les utilisateurs qui doivent
    beneficier de l'installation de raisin.
    * Si cette fonction est lancee avec les
    droits administrateurs et que l'utilisateur
    veut faire beneficier tout le monde de raisin,
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
                question="How do you want to install 'raisin'?",
                choix=[("Do you want an instance of 'raisin' start independently for "
                    "each user each time they log in, (so each user can configure "
                    "the behavior of the application as they wish) ?"),
                    ("Do you want a single instance of 'raisin' start a the "
                    "computer boot, (so the root user is the only user "
                    "that can to configure the behavior) ?")]):
            racine = "C:\\Users" if os.name == "nt" else "/home"
            for user in os.listdir(racine):
                yield os.path.join(racine, user)
        else:
            yield "all_users"
    else:
        yield os.path.expanduser("~")

def main():
    """
    Installe les elements fondamentaux
    pour le bon fonctionnement de l'application.
    N'agit pas de la même facon selon les droits.
    """
    with tools.Printer("Install raisin...") as p:
        
        # On donne les droits d'ecriture pour les mises a jour
        if tools.identity["has_admin"]:
            try:
                raisin_path = upgrade.find_folder()
            except OSError:
                pass
            else:
                for d, _, fs in os.walk(raisin_path):
                    os.chmod(d, 0o777)
                    for f in fs:
                        os.chmod(os.path.join(d, f), 0o777)

        # install_dependencies()
        actions = ["paranoiac", "normal", "altruistic", "custom"]
        action = actions[
            dialog.question_choix_exclusif(
                "Quel mode d'installation ?",
                ["paranoiac (maximum security)",
                 "normal (compromise between safety and efficiency)",
                 "altruistic (maximum performance)",
                 "custom (request your detailed opinion)"])]
        for home in _list_home():
            install_shortcut(home)
            install_settings(home, action)
            install_startup(home)

if __name__ == "__main__":
    main()
