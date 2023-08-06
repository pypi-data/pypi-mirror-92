# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# Local
from .utils import Utils, Flows

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

# Main

def new_package():
    Flows.new_package(Utils.get_arg(surpress_crash=True))

def upgrade():
    Flows.upgrade()

def publish():
    Flows.publish()

def publish_and_push():
    Flows.publish_and_push()

def clean_lines():
    Flows.clean_lines()


# Git

def push():
    Flows.push()

def fetch():
    Flows.fetch()

def pull():
    Flows.pull()


# Pip

def uninstall():
    Flows.uninstall(Utils.get_arg())

def install():
    Flows.install(Utils.get_arg())

def reinstall():
    Flows.reinstall(Utils.get_arg())


# New files

def create_install_file():
    Flows.create_install_file()

def create_new_api():
    Flows.create_new_api(Utils.get_arg())

def create_new_class():
    Flows.create_new_class(Utils.get_arg())

def create_new_enum():
    Flows.create_new_enum(Utils.get_arg())

def create_new_file():
    Flows.create_new_file(Utils.get_arg())

def create_new_flow():
    Flows.create_new_flow(Utils.get_arg())

def create_new_subpackage():
    Flows.create_new_subpackage(Utils.get_arg())


# ---------------------------------------------------------------------------------------------------------------------------------------- #
