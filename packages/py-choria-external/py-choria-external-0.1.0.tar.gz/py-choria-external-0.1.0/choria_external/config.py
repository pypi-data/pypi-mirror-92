import os


class Config:
    """ Class which handles reading settings from the plugin configuration file
    """

    CONFIG_DIR = '/etc/puppetlabs/mcollective/plugin.d/'

    def __init__(self, plugin_name):
        self.plugin_name = plugin_name
        self.config_file = os.path.join(os.environ.get('CHORIA_EXTERNAL_CONFIG', self.CONFIG_DIR), '{0}.cfg'.format(self.plugin_name))
        self.config = {}

    def config_exists(self):
        return os.path.exists(self.config_file)

    def read_config(self):
        """ Reads the configuration in from disk
        """
        if not self.config_exists():
            return

        with open(self.config_file, 'r') as fp:
            contents = fp.readlines()
            self.config = self.parse_config(contents)

    @staticmethod
    def parse_config(contents):
        """ Parses the configuration data

        :param contents: list[str] List of lines from the configuration file
        :return: dict[str,str]
        """
        config = {}

        for line in contents:
            line = line.lstrip().rstrip('\r\n')

            # Ignore comments
            if line.startswith('#'):
                continue

            # Ignore lines which do not contain key=value pairs
            if '=' not in line:
                continue

            key, _, value = line.partition('=')

            config[key.strip()] = value.lstrip()

        return config

    def __contains__(self, key):
        return key in self.config

    def __getitem__(self, key):
        return self.config[key]

    def get(self, key, default_value=None):
        return self.config.get(key, default_value)
