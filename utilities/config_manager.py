import configparser

class ConfigManager:
    
    @staticmethod
    def get_config_for_file(extension):
        config = configparser.ConfigParser(allow_no_value=True, delimiters=('=', ':'), comment_prefixes=('#', ';'))
        config.read('config.ini')
        
        for section in config.sections():
            if config[section].get("extension") == extension:
                return dict(config.items(section))

        return None
