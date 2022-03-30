# Setup your environment

## 1. Setup your config server

run the below command in your terminal

``` bash
docker-compose -f cfg_svr.yaml up -d
```

then login any one of these 3 mongodb to inintialize the RS(replica set). You can use terminal or mongodb compass to run the following command.

The host ip should not be localhost or 127.0.0.1, you can check your ip from `ifconfig` command on Linux or Mac, or check it in Network on Windows.

``` sh
mongosh mongodb://<Your Host IP>:40001
```

``` js
rs.initiate(
  {
    _id: "cfg_rs",
    members: [
      { _id : 0, host : "<Your Host IP>:40001" },
      { _id : 1, host : "<Your Host IP>:40002" },
      { _id : 2, host : "<Your Host IP>:40003" }
    ]
  }
)
```

## 2. Prepare your sharding dbs

You need to setup multiple shardings, for each sharding, you need to follow the steps below, just modify the text from `shard0` to `shardX`, and make sure there's no duplicated ports(edit the yaml file your self).

``` sh
docker-compose -f shard0.yaml up -d
```

Then login to `mongodb://<Your Host IP>:5000x` and run

``` js
// ALSO REMEMBER TO MODIFY THE PORTS
rs.initiate(
  {
    _id: "shard0_rs",
    members: [
      { _id : 0, host : "<Your Host IP>:50001" },
      { _id : 1, host : "<Your Host IP>:50002" },
      { _id : 2, host : "<Your Host IP>:50003" }
    ]
  }
)
```


## 3. Create the router

Run `router.yaml` as above, but **YOU NEED TO MODIFY IPS IN THIS FILE** 

e.g. my version is 

``` yaml
version: '3'

services:

  mongos:
    container_name: mongos
    image: mongo
    command: mongos --configdb cfg_rs/10.6.56.67:40001,10.6.56.67:40002,10.6.56.67:40003 --bind_ip 0.0.0.0 --port 27017
    ports:
      - 60000:27017
```

then

``` sh
docker-compose -f router.yaml up -d
```

and login to this router `mongodb://<YOUR HOST IP>:60000` and run

``` js
sh.addShard("shard0_rs/<YOUR HOST IP>:<PORT1>,<YOUR HOST IP>:<PORT2>,<YOUR HOST IP>:<PORT3>")
```

## 4. Play around with your env

literally, all following opeartions should run in the router mongo CLI, except you know what you're doing.

you can set zone based sharding

``` js
// let the router know shard0 is in NYC
sh.addShardToZone("shard0", "NYC")

// how to find data in NYC data center
db.shards.find({ tags: "NYC" })
```