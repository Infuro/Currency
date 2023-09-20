class Policy:
    def __init__(
            self,
            id,
            name,
            description,
            config,
            port_channel_id,
            max_frame_size):
        self.id = id
        self.name = name
        self.description = description
        self.config = config
        self.port_channel_id = port_channel_id
        self.max_frame_size = max_frame_size
