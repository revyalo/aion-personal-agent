import os


class Config:
    def __init__(self):
        self.provider = os.getenv("AION_PROVIDER", "mock")