from pdm.cli.commands.base import BaseCommand
from pdm.installers.installers import is_dist_editable


class FreezeCommand(BaseCommand):
    """Generate requirements.txt from local directory
    """

    def handle(self, project, options):
        working_set = project.environment.get_working_set()
        with open("requirements.txt", "w+") as f:
            for k, v in working_set.items():
                if not is_dist_editable(v):
                    f.write(f"{k}={v.version}\n")


def freeze_plugin(core):
    core.register_command(FreezeCommand, "freeze")
