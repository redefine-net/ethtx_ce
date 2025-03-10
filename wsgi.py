#  Copyright 2021 DAI Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os

from ethtx import EthTx, EthTxConfig
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from ethtx_ce import frontend, api

app = Flask(__name__)

ethtx_config = EthTxConfig(
    mongo_connection_string=os.getenv("MONGO_CONNECTION_STRING"),
    mongo_database=os.getenv("MONGODB_DB"),
    etherscan_api_key=os.getenv("ETHERSCAN_KEY"),
    web3nodes={
        "mainnet": dict(hook=os.getenv("MAINNET_NODE_URL", ""), poa=False),
        "goerli": dict(hook=os.getenv("GOERLI_NODE_URL", ""), poa=True),
    },
    default_chain="mainnet",
    etherscan_urls={
        "mainnet": "https://api.etherscan.io/api",
        "goerli": "https://api-goerli.etherscan.io/api",
    },
)

ethtx = EthTx.initialize(ethtx_config)

app.wsgi_app = DispatcherMiddleware(
    frontend.create_app(engine=ethtx, settings_override=EthTxConfig),
    {"/api": api.create_app(engine=ethtx, settings_override=EthTxConfig)},
)

if __name__ == "__main__":
    app.run()
