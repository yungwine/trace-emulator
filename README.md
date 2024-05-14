# Trace Emulator API

API to emulate transactions traces. Features:

* Cache account states for blocks. Very useful (and safe!) for emulation externals from mempool since there are a lot of
popular contracts that involved in many traces.
* Updates blockchain config every validation round so emulation will be as close to real as possible.
* High performance. The median value for emulation 10,000 real traces from mempool is 0.01s per trace, the average is 0.14s.

Now it's recommended to use this service with at least 3 private liteservers to emulate traces for all externals from mempool. 
However, you can filter mining externals (not emulate them) and the load will drop several times.

## ENV

Create `.env` file with the following content:

```
PORT=12123  # port for the API
CONFIG_PATH='config.json'  # path to config with liteservers
MAX_REQ_PER_PEER=30  # maximum amount of requests per liteserver
LOGGING='INFO'  # logging level
WORKERS=10  # amount of workers for uvicorn. can be equal or less than number of cores
EMULATION_CACHE_SEC=5  # seconds to cache emulation result
```


## Installation

After cloning the repository and setting up environment variables run docker-compose:

`docker compose up --build -d`
