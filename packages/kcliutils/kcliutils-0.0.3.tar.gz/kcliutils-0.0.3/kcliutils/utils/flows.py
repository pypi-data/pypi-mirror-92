# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List
import os

# Pip
from kcu import kpath, strio, sh
from kdependencies import Dependencies, InstalledPackage

# Local
from .utils import Utils
from .prompt import Prompt
from .texts import new_api, new_class, new_enum, new_license, file, flow, gitignore, new_readme, updated_readme, new_setup, updated_setup, new_install_dependencies_file

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Flows ------------------------------------------------------------- #

class Flows:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    # Main

    @classmethod
    def new_package(cls, package_name: Optional[str]):
        input('Ensure you\'re in the correct path: \'{}\''.format(os.getcwd()))

        res = Utils.get_args(0)
        package_name = res[0] if res > 0 else None
        config = Utils.get_config(True)
        package_name, description = Prompt.new_package(package_name, os.getcwd().split(os.sep)[-1])

        if not os.path.exists(Utils.setup_file_path()):
            Utils.create_file(Utils.setup_file_path(), new_setup(
                package_name=package_name,
                min_python_version=config.default_min_python_version,
                max_python_version=config.default_max_python_version,
                license_str='License :: OSI Approved :: MIT License'
            ))

        if not os.path.exists(Utils.readme_path()):
            cls.create_new_readme(package_name, Utils.get_full_git_repo_name(), description, open=False)

        if not os.path.exists(Utils.gitignore_path()):
            cls.create_new_gitignore(open=False)

        if not os.path.exists(Utils.demo_path()):
            Utils.create_file(Utils.demo_path())

        cls.create_new_subpackage(os.path.join(package_name, 'models'), create_class=True)
        cls.create_new_subpackage(os.path.join(package_name, 'core'), create_class=True)
        cls.create_new_subpackage(package_name, create_class=True)

    @classmethod
    def upgrade(cls, ensure_path: bool = True, clean_lines: bool = True):
        if ensure_path:
            Utils.ensure_and_get_path()

        if clean_lines:
            cls.clean_lines(ensure_path=False)

        old_setup_str = strio.load(Utils.setup_file_path())
        old_readme_str = strio.load(Utils.readme_path())
        demo_str = strio.load(Utils.demo_path())

        print('Getting dependencies...')
        dependencies = Dependencies.get()

        updated_setup_str = updated_setup(old_setup_str, dependencies)
        updated_readme_str = updated_readme(old_readme_str, demo_str, dependencies)

        Utils.create_file(Utils.setup_file_path(), updated_setup_str, overwrite=True)
        Utils.create_file(Utils.readme_path(), updated_readme_str, overwrite=True)

        cls.create_install_file(dependencies, open=False)

    @classmethod
    def publish(cls, ensure_path: bool = True, clean_lines: bool = True):
        if ensure_path:
            Utils.ensure_and_get_path()

        cls.upgrade(ensure_path=False, clean_lines=clean_lines)
        current_package_name = Utils.get_current_package_name()

        print('Publishing \'{}\' to pypi'.format(current_package_name))
        Utils.publish()

        print('Reinstalling \'{}\''.format(current_package_name))
        cls.reinstall(current_package_name)

    @classmethod
    def publish_and_push(cls, message: Optional[str] = None, clean_lines: bool = True):
        cls.publish(ensure_path=True, clean_lines=clean_lines)
        cls.push(ensure_path=False, clean_lines=False)

    @classmethod
    def clean_lines(cls, ensure_path: bool = True):
        if ensure_path:
            Utils.ensure_and_get_path()

        for p in kpath.file_paths_from_folder(os.getcwd(), allowed_extensions=cls.__allowed_extesions()):
            with open(p, 'r') as f:
                org_text = f.read()
                text = '\n'.join([l.rstrip() for l in org_text.strip().split('\n')]) + '\n'

            if org_text != text:
                print('Cleaning: \'{}\''.format(p))

                with open(p, 'w') as f:
                    f.write(text)


    # Git

    @classmethod
    def push(cls, message: Optional[str] = None, ensure_path: bool = True, clean_lines: bool = True):
        if ensure_path:
            Utils.ensure_and_get_path()

        if clean_lines:
            cls.clean_lines(ensure_path=False)

        print(sh.sh('git add .', debug=True))
        print(sh.sh('git commit -a -m \'{}\''.format(message or Utils.get_config(True).default_commit_message), debug=True))
        print(sh.sh('git push', debug=True))

    @staticmethod
    def fetch():
        print(sh.sh('git fetch', debug=True))

    @classmethod
    def pull(cls):
        cls.fetch()
        print(sh.sh('git pull', debug=True))


    # Pip install

    @staticmethod
    def uninstall(package: str):
        Utils.pip('uninstall -y {}'.format(package))

    @staticmethod
    def install(package: str):
        Utils.pip('install -U {}'.format(package))

    @classmethod
    def reinstall(cls, package: str):
        cls.uninstall(package)
        cls.install(package)


    # New files

    @staticmethod
    def create_install_file(dependencies: Optional[List[InstalledPackage]] = None, open: bool = True):
        file_path = Utils.install_dependencies_path()

        if not dependencies:
            if os.path.exists(file_path):
                os.remove(file_path)

            return

        Utils.create_file(file_path, new_install_dependencies_file(dependencies), overwrite=True)

        if open:
            Utils.vscode_open(file_path)

    @staticmethod
    def create_new_api(name: str, open: bool = True):
        _, file_path, _, _class = Utils.get_paths_name_class(name)
        Utils.create_file(file_path, new_api(_class))

        if open:
            Utils.vscode_open(file_path)

    @staticmethod
    def create_new_class(name: str, open: bool = True):
        _, file_path, _, _class = Utils.get_paths_name_class(name)
        Utils.create_file(file_path, new_class(_class))

        if open:
            Utils.vscode_open(file_path)

    @staticmethod
    def create_new_enum(name: str, open: bool = True):
        _, file_path, _, _class = Utils.get_paths_name_class(name)

        Utils.create_file(file_path, new_enum(_class))

        if open:
            Utils.vscode_open(file_path)

    @staticmethod
    def create_new_file(name: str, open: bool = True):
        _, file_path, _, _ = Utils.get_paths_name_class(name)

        Utils.create_file(file_path, file)

        if open:
            Utils.vscode_open(file_path)

    @staticmethod
    def create_new_flow(name: str, open: bool = True):
        _, file_path, _, _ = Utils.get_paths_name_class(name)

        Utils.create_file(file_path, flow)

        if open:
            Utils.vscode_open(file_path)

    @staticmethod
    def create_new_gitignore(open: bool = True):
        Utils.create_file(Utils.gitignore_path(), gitignore)

        if open:
            Utils.vscode_open(Utils.gitignore_path())

    @staticmethod
    def create_new_readme(
        package_name: str,
        full_repo_name: Optional[str] = None,
        description: Optional[str] = None,
        open: bool = False
    ):
        file_path = Utils.readme_path()
        Utils.create_file(file_path, new_readme(package_name=package_name, full_repo_name=full_repo_name, description=description))

        if open:
            Utils.vscode_open(file_path)

    @classmethod
    def create_new_subpackage(cls, relative_folder_path: str, create_class: bool = True):
        _, init_file_path, _, _ = Utils.get_paths_name_class(Utils.init_file_path(relative_folder_path))

        if create_class:
            _, _, class_file_name, _class = Utils.get_paths_name_class(relative_folder_path)
            cls.create_new_class(os.path.join(relative_folder_path, class_file_name), open=False)

            Utils.create_file(init_file_path, 'from .{} import {}'.format(class_file_name, _class))
        else:
            Utils.create_file(init_file_path, '')

    # ------------------------------------------------------ Private properties ------------------------------------------------------ #



    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    @staticmethod
    def __allowed_extesions() -> List[str]:
        return [
            '.py',
            '.js',
            '.ts',
            '.json'
        ]


# ---------------------------------------------------------------------------------------------------------------------------------------- #
