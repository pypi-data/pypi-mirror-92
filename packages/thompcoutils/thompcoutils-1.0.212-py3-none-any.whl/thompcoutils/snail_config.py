import os
from thompcoutils.config_utils import EmailConnectionConfig
from thompcoutils.config_utils import ConfigException
from thompcoutils.config_utils import ConfigManager
from thompcoutils.config_utils import PiConfig


class VoltageConfig:
    section_heading = "fence voltages"
    min_trigger_voltage_tag = "min trigger percent"
    max_trigger_voltage_tag = "max trigger percent"
    voltage_check_frequency_tag = "voltage check frequency"

    def __init__(self, cfg_mgr):
        self.min_trigger_voltage = cfg_mgr.read_entry(section=VoltageConfig.section_heading,
                                                      entry=VoltageConfig.min_trigger_voltage_tag,
                                                      default_value=0.1,
                                                      notes='the minimum voltage (percentage) to trigger a low voltage')
        self.max_trigger_voltage = cfg_mgr.read_entry(section=VoltageConfig.section_heading,
                                                      entry=VoltageConfig.max_trigger_voltage_tag,
                                                      default_value=0.9,
                                                      notes='the maximum voltage (percentage) to trigger a high voltage')
        self.voltage_check_frequency = cfg_mgr.read_entry(section=VoltageConfig.section_heading,
                                                          entry=VoltageConfig.voltage_check_frequency_tag,
                                                          default_value=0.01,
                                                          notes='frequency (in seconds) to check voltages')


class WebConfig:
    section = 'www'
    port_tag = 'port'
    domain_tag = 'domain'
    username_tag = 'username'
    password_tag = 'password'

    def __init__(self, cfg_mgr, port=8080, domain='thompco.com', username='admin', password='admin'):
        """
        WifiConfig defines the data for the wpa_suplicant file
        :param cfg_mgr: the ConfigManager
        :param port: port to listen on
        :param domain: domain for this server
        """
        self.username = cfg_mgr.read_entry(WebConfig.section, WebConfig.username_tag, username)
        self.password = cfg_mgr.read_entry(WebConfig.section, WebConfig.password_tag, password)
        self.port = cfg_mgr.read_entry(WebConfig.section, WebConfig.port_tag, port)
        self.domain = cfg_mgr.read_entry(WebConfig.section, WebConfig.domain_tag, domain)


class SnailBootConfig(PiConfig):
    def __init__(self):
        """
        SnailBootConfig reads the initial boot configuration file from the /boot folder
        """
        super(SnailBootConfig, self).__init__(title='Snail Patrol Boot Configuration')
        self.email_config = EmailConnectionConfig(self)
        self.web_config = WebConfig(self)
        self.fence_voltages = VoltageConfig(self)

    def write_snail_config_file(self):
        """
        This function writes other data to the snail_patrol config file
        :return: None
        """


def main():
    """
    This function reads the configuration file (if it exists) and makes the appropriate changes to the other
    files
    :return: None
    """
    try:
        PiConfig._boot_folder = "/tmp"
        PiConfig._wpa_supplicant_file = '/tmp/wpa_supplicant.config'
        PiConfig._host_name_file = '/tmp/hostname'
        test_file = "snail_config.cfg"
        if os.path.exists(test_file):
            os.remove(test_file)
        snail_config = SnailConfig(config_file=test_file)

        #snail_config.write_wpa_supplicant()
        #snail_config.write_host_files()
        #snail_config.write_snail_config_file()

    except ConfigException:
        pass


class SnailConfig(ConfigManager):
    def __init__(self, config_file):
        new_file = not os.path.isfile(config_file)
        super(SnailConfig, self).__init__(file_name=config_file, title='Snail Patrol Run Configuration',
                                          create=new_file)
        self.email_config = EmailConnectionConfig(self)
        self.web_config = WebConfig(self)
        self.fence_voltages = VoltageConfig(self)

        if new_file:
            self.write(out_file=config_file, overwrite=True, stop=True)


if __name__ == '__main__':
    main()