""" Contains functionality for configuration of pipeline elements """
import configargparse


class ConfigurationHelper:
    """
    Helper class for parsing pipeline element configuration from multiple sources.
    Provides a thin wrapper around the `configargparse` library.
    """

    def __init__(self):
        self.config = None
        self._parser = configargparse.ArgParser(
            default_config_files=["weasel-pipeline.conf"]
        )
        self._parser.add("-c", "--config", is_config_file=True, help="config file path")
        self._parser.add(
            "--amqp_uri",
            env_var="AMQP_URI",
            required=True,
            help="URL of RabbitMQ server",
        )

    def add_argument(
        self,
        keyword: str,
        argument_type: type = str,
        required: bool = True,
        help_text: str = None,
    ) -> None:
        """
        Add an argument to the configuration parser.

        :param keyword: The keyword for this argument, i.e. `--<keyword>` on the command line
        :param argument_type: The type of the argument value (e.g. str, int)
        :param required: Whether or not this argument is required
        :param help_text: The help text which is shown for this argument
        """
        self._parser.add(
            "--{}".format(keyword),
            env_var="{}".format(keyword.upper()),
            type=argument_type,
            required=required,
            text=help_text,
        )

    def parse(self) -> None:
        """
        Parse the passed arguments and store the result in the `config` attribute.
        """
        self.config = self._parser.parse_args()
