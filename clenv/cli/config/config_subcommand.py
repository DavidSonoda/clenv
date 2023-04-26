from .config_manager import ConfigManager
import click


INDEX_FILE_PATH = "~/.clenv-config-index.json"
EMPTY_INDEX_JSON = {"profiles": {}}


# Create a group
@click.group(help="Manage config files")
def config():
    pass


@click.option(
    "--showpath", "-v", is_flag=True, help="Show config file path for the profile"
)
@config.command(help="List all config profiles")
def list(showpath):
    config_manager = ConfigManager(INDEX_FILE_PATH)
    if not config_manager.profile_has_initialized():
        # Prompt the user to initalize the profile by inputting a profile name, the default is 'default'
        # Solution
        profile_name = click.prompt("Please input a profile name", default="default")
        config_manager.initialize_profile(profile_name)

    active_profiles = config_manager.get_active_profile()
    non_active_profiles = config_manager.get_non_active_profiles()
    for profile in active_profiles:
        # Print the active profile name with '(active)' at the end, print it in green color
        click.echo(click.style(f'{profile["profile_name"]} [active]', fg="green"))
        if showpath:
            click.echo(click.style(f'  {profile["file_path"]}'))
    for profile in non_active_profiles:
        # Print the non-active profile name, print it in yellow color
        click.echo(click.style(f'{profile["profile_name"]}', fg="yellow"))
        if showpath:
            click.echo(click.style(f'  {profile["file_path"]}'))


# Checkout the profile name specified by the user, and set it as the default profile.
# If the profile name is not found in the index file, print an error message and exit
# Solution
@config.command(name="checkout", help="Checkout another profile")
@click.argument("profile_name")
def checkout(profile_name):
    config_manager = ConfigManager(INDEX_FILE_PATH)
    if not config_manager.has_profile(profile_name=profile_name):
        click.echo(f"Profile {profile_name} does not exist")
        return
    active_profile = config_manager.get_active_profile()
    if active_profile[0]["profile_name"] == profile_name:
        click.echo(f"Profile {profile_name} is already active")
        return
    else:
        config_manager.set_active_profile(profile_name)
        click.echo(f'Profile "{profile_name}" is now active')


# Create a new profile, the profile name is specified by the user
# If the profile name is already in the index file, print an error message and exit
# Solution
@click.argument("profile_name", required=True)
@click.option("--base", "-b", help="Base profile name")
@config.command(help="Create a new profile")
def create(profile_name, base):
    config_manager = ConfigManager(INDEX_FILE_PATH)
    if config_manager.has_profile(profile_name=profile_name):
        click.echo(f"Profile {profile_name} already exists")
        return
    config_manager.create_profile(profile_name, base)
    click.echo(f"Profile {profile_name} created")


# Delete the profile specified by the user, if the profile is the default profile, print an error
# message and exit. If the profile is not found in the index file, print an error message and exit.
# Solution
@click.argument("profile_name", required=True)
@config.command(name="del", help="Delete a profile")
def delete(profile_name):
    config_manager = ConfigManager(INDEX_FILE_PATH)
    if not config_manager.has_profile(profile_name=profile_name):
        click.echo(f"Profile {profile_name} does not exist")
        return
    if config_manager.is_active_profile(profile_name):
        click.echo(
            f"Profile {profile_name} is active, only non-active profiles can be deleted"
        )
        return
    config_manager.delete_profile(profile_name)
    click.echo(f"Profile {profile_name} deleted")


# Rename profile
@config.command(help="Rename a profile")
@click.argument("old_profile_name", required=True)
@click.argument("new_profile_name", required=True)
def rename(old_profile_name, new_profile_name):
    config_manager = ConfigManager(INDEX_FILE_PATH)
    if not config_manager.has_profile(profile_name=old_profile_name):
        click.echo(f"Profile {old_profile_name} does not exist")
        return
    if config_manager.has_profile(profile_name=new_profile_name):
        click.echo(f"Profile {new_profile_name} already exists")
        return
    config_manager.rename_profile(old_profile_name, new_profile_name)
    click.echo(f"Profile {old_profile_name} renamed to {new_profile_name}")


# Reinitialize the api section of the config file. The argument is the hocon formatted
# string that will be used to replace the api section of the config file.
@click.argument("base_profile", required=True)
@config.command(help="Reinitialize the api section of the config file")
def reinit(base_profile):
    click.echo("Please paste your multi-line configuration and press Enter:")
    config = read_multiline()

    config_manager = ConfigManager(INDEX_FILE_PATH)
    config_manager.reinitialize_api_config(base_profile, config)


def read_multiline():
    lines = []
    while True:
        try:
            line = input()
            if not line:
                break
            lines.append(line)
        except EOFError:
            break

    return "\n".join(lines)
