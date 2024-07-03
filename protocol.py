import bittensor as bt
from pydantic import BaseModel

class ProfileData(BaseModel):
    github_exists: bool
    github_repos: int
    github_commits: int
    linkedin_exists: bool
    ethereum_balance: float
    bittensor_staked_balance: float
    # Add other fields as necessary

class ProfileSynapse(bt.Synapse):
    def __init__(self, input_data: ProfileData):
        self.input_data = input_data

    def serialize(self):
        return self.input_data.json()

    @staticmethod
    def deserialize(data):
        input_data = ProfileData.parse_raw(data)
        return ProfileSynapse(input_data)
