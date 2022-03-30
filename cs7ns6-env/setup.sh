#!env bash

############# CONFIGS #############

HOST=host.docker.internal
DIR=$(dirname "$0")
DB=cs7ns6
COLLECTION=athlete
COUNTRIES=(
  "IE"
  "GB"
  "DE"
)
SLEEP=5

############### END ###############

function create_containers() {
  # config server
  docker-compose -f ${DIR}/cfg_svr.yaml up -d

  # shardings
  i=0
  for COUNTRY in "${COUNTRIES[@]}"; do
    sed "s/__IDX__/${i}/g" ${DIR}/_shard_template.yaml >${DIR}/shard_${i}.yaml
    i=$((i + 1))
  done

  for SHARD in $(find ${DIR} -name 'shard*.yaml'); do
    docker-compose -f $SHARD up -d
  done

  # router
  docker-compose -f ${DIR}/router.yaml up -d
}

function setup_replica_sets() {
  echo "rs.initiate(
    {
      _id: \"cfg_rs\",
      members: [
        { _id : 0, host : \"${HOST}:40001\" },
        { _id : 1, host : \"${HOST}:40002\" },
        { _id : 2, host : \"${HOST}:40003\" }
      ]
    }
  )" | mongosh mongodb://localhost:40001

  i=0
  for SHARD in $(find ${DIR} -name 'shard*.yaml'); do
    echo "rs.initiate(
      {
        _id: \"shard${i}_rs\",
        members: [
          { _id : 0, host : \"${HOST}:500${i}1\" },
          { _id : 1, host : \"${HOST}:500${i}2\" },
          { _id : 2, host : \"${HOST}:500${i}3\" }
        ]
      }
    )" | mongosh mongodb://localhost:500${i}1
    i=$((i + 1))
    sleep ${SLEEP}
  done
}

function setup_router() {
  i=0
  for SHARD in $(find ${DIR} -name 'shard*.yaml'); do
    echo "sh.addShard(\"shard${i}_rs/${HOST}:500${i}1,${HOST}:500${i}2,${HOST}:500${i}3\")" | mongosh mongodb://localhost:60000
    i=$((i + 1))
    sleep ${SLEEP}
  done
}

function setup_db() {
  echo "
    use ${DB}
    db.createCollection(\"${COLLECTION}\")
  " | mongosh mongodb://localhost:60000
  sleep ${SLEEP}
}

function setup_shardings() {
  echo "sh.enableSharding(\"${DB}\")" | mongosh mongodb://localhost:60000

  sleep ${SLEEP}

  i=0
  for SHARD in $(find ${DIR} -name 'shard_*.yaml'); do
    echo "sh.addShardToZone(\"shard${i}_rs\", \"${COUNTRIES[$i]}\")
    sh.updateZoneKeyRange(\"${DB}.athlete\", 
        { 
          \"nationality\": \"${COUNTRIES[$i]}\", 
          \"email\": MinKey 
        }, 
        { 
          \"nationality\": \"${COUNTRIES[$i]}\", 
          \"email\": MaxKey 
        }, 
        \"${COUNTRIES[$i]}\"
    )" | mongosh mongodb://localhost:60000
    i=$((i + 1))

    sleep ${SLEEP}

  done

  sleep ${SLEEP}

  echo "sh.shardCollection(\"${DB}.athlete\", { \"nationality\": 1, \"email\": 1 } )" | mongosh mongodb://localhost:60000
}

function main() {
  create_containers
  setup_replica_sets
  setup_router
  setup_db
  setup_shardings
}

main
