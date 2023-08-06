# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List

# Pip
from kdependencies import InstalledPackage
from kcu import strings

# Local
from .core_texts import readme
from .utils import multi_replace

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def updated_readme(
    readme: str,
    demo: Optional[str],
    dependencies: Optional[List[InstalledPackage]]
) -> str:
    if demo:
        usage = strings.between(readme, '## Usage', '##')

        if usage:
            readme.replace(usage.strip(), '\n\n~~~~python\n{}\n~~~~\n\n'.format(demo.strip()))

    if dependencies:
        old_dependencies = strings.between(readme, '## Dependencies', '##')

        if old_dependencies:
            readme.replace(old_dependencies.strip(), ', '.join(['[{}]({})'.format(d.name, 'https://pypi.org/project/{}'.format(d.name) if not d.private else d.home_url) for d in dependencies]))

    return readme.strip()

def new_readme(
    package_name: str,
    full_repo_name: Optional[str] = None,
    description: Optional[str] = None,
    dependencies: Optional[List[InstalledPackage]] = None
) -> str:
    return multi_replace(
        readme,
        {
            '[PACKAGE_NAME]': package_name,
            '[SHIELDS]': __create_shields(package_name, full_repo_name) if full_repo_name else '',
            '[DESCRIPTION]': description or '',
            '[DEPENDENCIES]': ', '.join(['[{}]({})'.format(d.name, 'https://pypi.org/project/{}'.format(d.name) if not d.private else d.home_url) for d in dependencies]) if dependencies else ''
        }
    )


# ----------------------------------------------------------- Private methods ------------------------------------------------------------ #

def __create_shields(
    package_name: str,
    full_repo_name: Optional[int]
):
    return ' '.join(
        [
            __shield('GitHub - last commit', 'github/last-commit/{}'.format(full_repo_name)),
            __shield('GitHub - commit activity', 'github/commit-activity/m/{}'.format(full_repo_name)),
            __shield('GitHub - code size in bytes', 'github/languages/code-size/{}'.format(full_repo_name)),
            __shield('GitHub - repo size', 'github/repo-size/{}'.format(full_repo_name)),
            __shield('GitHub - lines of code', 'tokei/lines/github/{}'.format(full_repo_name)),
            __shield('GitHub - license', 'github/license/{}'.format(full_repo_name)),

            __shield('PyPI - Python Version', 'pypi/pyversions/{}?logo=pypi'.format(package_name)),
            __shield('PyPI - Downloads', 'pypi/dm/{}?logo=pypi'.format(package_name))
        ]
    )

def __shield(name: str, url_data: str, style: str = 'flat-square') -> str:
    return '![{}](https://img.shields.io/{}{}style={})'.format(name, url_data, '&' if '?' in url_data else '?', style)


# ---------------------------------------------------------------------------------------------------------------------------------------- #
