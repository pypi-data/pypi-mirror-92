"""Main module.

- Generate list of modules with values
- Lookup directories and fetch information
- Aggregate every generated templates
- Add metadata
- Output markdown

"""
from ansible_mkdocs import role


def main():
    default_modules = fetch_default_modules()
    role = role.Role(path, **extras)
    role.introspect(verbose=False)
    # component:
    #   component_type: vars
    #   content:
    #     executable_directory:
    #       value: /opt/bin
    #       comment: "Install in default common installation directory."
    #       file: main.yml
    #

    #  role.set_components(role.fetch_components())
    #  Role.render(template=None)
    #  
    # https://jinja.palletsprojects.com/en/2.11.x/templates/#macros

    # can lead to:
    #   Playbook(roles)
    #   playbook.render(template=None) (then for component component.render())

    documentation = """"""  # playbook.render(template=None)
    print(documentation)
