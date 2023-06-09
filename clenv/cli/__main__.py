import click

# Inmport the user and config commands
from .user import user_subcommand
from .config import config_subcommand
from .task import task_subcommand


@click.group()
def clenv():
    pass


clenv.add_command(config_subcommand.config)
clenv.add_command(user_subcommand.user)
clenv.add_command(task_subcommand.task)


def main():
    clenv()


if __name__ == "__main__":
    main()
