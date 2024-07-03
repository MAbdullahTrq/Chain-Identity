# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# developer: Avento Labs
# Copyright © 2023 Avento Labs

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


import time

# Bittensor
import bittensor as bt

# import base validator class which takes care of most of the boilerplate
from template.base.validator import BaseValidatorNeuron
from template.validator import forward
from protocol import ProfileSynapse



class Validator(BaseValidatorNeuron):
    def forward(self, synapse, **kwargs):
        profile_data = self.collect_profile_data(synapse.input_data)
        synapse = ProfileSynapse(profile_data)
        responses = self.request(synapse)
        scores = [response["score"] for response in responses]
        mean_score = sum(scores) / len(scores)
        self.submit_scores(mean_score, responses)
        return mean_score
    
    def collect_profile_data(self, input_data):
        # Implement logic to collect profile data
        github_exists = self.check_github(input_data.github_username)
        github_repos = self.get_github_repos(input_data.github_username)
        github_commits = self.get_github_commits(input_data.github_username)
        linkedin_exists = self.check_linkedin(input_data.linkedin_username)
        ethereum_balance = self.get_ethereum_balance(input_data.ethereum_address)
        bittensor_staked_balance = self.get_bittensor_staked_balance(input_data.bittensor_address)
        
        return ProfileData(
            github_exists=github_exists,
            github_repos=github_repos,
            github_commits=github_commits,
            linkedin_exists=linkedin_exists,
            ethereum_balance=ethereum_balance,
            bittensor_staked_balance=bittensor_staked_balance
        )

    def check_github(self, username):
        response = requests.get(f"https://api.github.com/users/{username}")
        return response.status_code == 200

    def get_github_repos(self, username):
        response = requests.get(f"https://api.github.com/users/{username}/repos")
        if response.status_code == 200:
            return len(response.json())
        return 0

    def get_github_commits(self, username):
        response = requests.get(f"https://api.github.com/users/{username}/events")
        if response.status_code == 200:
            events = response.json()
            return sum(1 for event in events if event["type"] == "PushEvent")
        return 0

    def check_linkedin(self, username):
        # LinkedIn API logic here
        return True

    def get_ethereum_balance(self, address):
        # Ethereum API logic here
        return 0.0

    def get_bittensor_staked_balance(self, address):
        # Bittensor API logic here
        return 0.0

    def submit_scores(self, mean_score, responses):
        # Submit the computed scores to the blockchain
        pass


# The main function parses the configuration and runs the validator.
if __name__ == "__main__":
    with Validator() as validator:
        while True:
            bt.logging.info(f"Validator running... {time.time()}")
            time.sleep(5)
