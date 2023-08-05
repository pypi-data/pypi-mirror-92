import os, json

DEFAULT_DELETE_ATER = 20


class Configurator:
    def __init__(self, config_path):
        self.config_path = config_path

    def create_file_if_not_exist(self):
        if not os.path.exists(self.config_path):
            with open(self.config_path, "w"): pass

    def read_config(self) -> dict:
        self.create_file_if_not_exist()
        with open(self.config_path) as config_json:
            config_data = json.load(config_json)

        return config_data

    def write_config(self, config_json):
        self.create_file_if_not_exist()
        with open(self.config_path, "w") as outfile:
            json.dump(config_json, outfile, indent=4)

    def get_auto_delete_duration(self, channel_id) -> int:
        try:
            auto_delete = self.read_config()["auto_delete"]
            duration = int(auto_delete[str(channel_id)])
            if duration == -1:
                duration = None
            return duration
        except:
            return DEFAULT_DELETE_ATER

    def save_auto_delete_duration(self, channel_id, duration: int):
        config = self.read_config()
        try:
            config_autodelete = config["auto_delete"]
        except:
            config['auto_delete'] = {}

        config["auto_delete"][str(channel_id)] = duration
        self.write_config(config)
