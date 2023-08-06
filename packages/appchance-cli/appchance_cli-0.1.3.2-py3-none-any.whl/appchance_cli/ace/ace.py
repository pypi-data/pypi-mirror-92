
import os, sys
import logging
import subprocess
from inspect import isclass
from importlib import import_module

logger = logging.getLogger(__name__)

envs = os.environ


class HelperCommander:
    @staticmethod
    def shell_cmd(cmd, envs_dict):
        logger.info(f"Running shell command: {cmd}")
        subprocess.Popen(cmd, shell=True, universal_newlines=True, env=envs_dict).wait()

    @staticmethod
    def import_plugins():
        sys.path.insert(0, os.getcwd())
        try:
            module = import_module(f"ace")
        except ModuleNotFoundError:
            return {}

        results = {}
        plugin_names = [attr_name for attr_name in dir(module) if "Controller" in attr_name]
        for plugin_name in plugin_names:
            plugin = getattr(module, plugin_name)
            base_cmd = getattr(plugin, "BASE_CMD", f"main#{plugin_name}")
            results[base_cmd] = plugin if isclass(plugin) else ...
        return results


class AppchanceCLI:

    def __init__(self, sub_commands):
        for cmd, controller in sub_commands.items():
            setattr(self, cmd, controller)

    @staticmethod
    def build(parallel=True, docker_cli=True, buildkit=True, path=None):
        """ Build docker-compose project. Use DOCKER_CLI and BuildKit by default.
        """
        envs.update({
            "COMPOSE_DOCKER_CLI_BUILD": "1" if docker_cli else "0",
            "DOCKER_BUILDKIT": "1" if buildkit else "0",
        })
        path_input = f" -f {path}/docker-compose.yml" if path else ""
        parallel_input = " --parallel" if parallel else ""
        HelperCommander.shell_cmd(
            f"docker-compose --log-level ERROR {path_input} build --compress {parallel_input}", envs)

    @staticmethod
    def up(detached=False):
        """ Start docker compose project up. """
        HelperCommander.shell_cmd(
            f"docker-compose up {'-d' if detached else ''}", envs)

    @staticmethod
    def down():
        """ Stop docker compose project. """
        HelperCommander.shell_cmd(
            "docker-compose down", envs)

    @staticmethod
    def shell():
        """ Open django shell. """
        HelperCommander.shell_cmd(
            "docker-compose exec api python manage.py shell_plus", envs)

    @staticmethod
    def bash():
        """ Open django shell. """
        HelperCommander.shell_cmd(
            "docker-compose exec api bash", envs)

    @staticmethod
    def test():
        """ Run tests. """
        HelperCommander.shell_cmd(
            "docker-compose exec api pytest", envs)

    @staticmethod
    def migrate():
        """ Migrate DB to new schema. """
        HelperCommander.shell_cmd(
            "docker-compose exec api python manage.py migrate", envs)

    @staticmethod
    def makemigrations():
        """ Generate Django migrations. """
        HelperCommander.shell_cmd(
            "docker-compose exec api python manage.py makemigrations", envs)
