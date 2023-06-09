import click

# Import generate_password from user.user_manager
import bcrypt
import os, re
import json
import base64
from pyhocon import ConfigFactory, HOCONConverter


@click.group(help="Privately hosted clearml server user helper tools")
def user():
    pass


# Write a command to generate a user config file ending with .conf in hocon format
# The command should take a username and a password as arguments,
# Encrypt the password using UserManager.generate_password() and write the username and encrypted password to the config file
# The config file should be named after the username and saved to home directory
@user.command(help="Generate a user password")
@click.argument("username", required=True)
@click.argument("password", required=False)
def genpass(username, password):
    try:
        if password is None:
            password = click.prompt("Create a password for the user", hide_input=True)
        cipher_pw = generate_password(password)

        config_dict = {
            "username": username,
            "password": base64.b64encode(cipher_pw).decode("utf-8"),
        }
        config = ConfigFactory.from_dict(config_dict)
        # Save the clearml-user.conf file in the home directory
        path = os.path.expanduser(f"~/clearml-server-{username}.conf")
        with open(path, "w") as f:
            f.write(HOCONConverter.to_hocon(config))

        click.echo(json.dumps(config_dict, indent=4))
        # Print the file path in green color
        click.echo(
            click.style(
                f"User name and cipher password config saved to {path}, please send the config file to server admin",
                fg="green",
            )
        )

    except ValueError as e:
        click.echo(click.style(str(e), fg="red"))
        return


# Generate a cipher text password from a plain text password using bcrypt, reject the
# password if it is not strong enough
def generate_password(plain_text_password):
    # Assert the plain text password is at least 8 characters long, must contain a
    # number, and must contain a upper case letter and a lower case letter
    valid = check_string(plain_text_password)
    if not valid:
        raise ValueError(
            "Password must be at least 8 characters long, must contain a number, and must contain a upper case letter and a lower case letter"
        )
    return bcrypt.hashpw(plain_text_password.encode("utf-8"), bcrypt.gensalt())


def check_string(string):
    # Check if the string contains at least one upper case letter, one lower case letter, one number, and is at least 8 characters long
    regex = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
    match = regex.match(string)
    return match is not None
