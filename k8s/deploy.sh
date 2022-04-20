#!bash

############# CONFIGS #############

DIR=$(dirname "$0")
DB=cs7ns6
COLLECTION=athlete
LOCATIONS=(
  "ie"
  "gb"
  "de"
)
SHARD_SVR_REPLICAS=3

############### END ###############

function generate-shards() {
  # render shard stateful set
  for LOCATION in "${LOCATIONS[@]}"; do
    sed "s/__LOCATION__/${LOCATION}/g" ${DIR}/__mongo.shard.sts.template > ${DIR}/mongo.shard.${LOCATION}.sts.yaml
  done

  cp ${DIR}/__mongo.cm.template ${DIR}/mongo.cm.yaml
  LOCATIONS_WITH_COMMA=$(printf '"%s",' "${LOCATIONS[@]}")
  LOCATIONS_WITH_COMMA=${LOCATIONS_WITH_COMMA%,}
  sed -i "s/__LOCATIONS__/${LOCATIONS_WITH_COMMA}/g" ${DIR}/mongo.cm.yaml
  sed -i "s/__SHARD_SVR_REPLICAS__/${SHARD_SVR_REPLICAS}/g"  ${DIR}/mongo.cm.yaml
  sed -i "s/__DB__/${DB}/g"  ${DIR}/mongo.cm.yaml
  sed -i "s/__COLLECTION__/${COLLECTION}/g"  ${DIR}/mongo.cm.yaml
}

function deploy() {
  kubectl apply -f ${DIR}
}

function cleanup() {
  kubectl delete -f ${DIR}
  kubectl get pvc | awk 'NR>1 {print $1}' | xargs kubectl delete pvc
  rm ${DIR}/mongo.shard.*.sts.yaml 
}

function wait-pod-running() {
  echo -n "Wait all pods are ready"
  ALL_DONE=false
  until [[ $ALL_DONE = true ]]; do
    ALL_STATUS=$(kubectl get pod | awk 'NR>1 {print $3}')
    ALL_DONE=true
    for STATUS in $ALL_STATUS; do
      if [[ $STATUS != "Running" ]]; then
        ALL_DONE=false
      fi
    done

    sleep 3
    echo -n "."
  done
  echo ""
  echo -n "Wait all mongodbs are ready"
  for ((i=0;i<10;i++)); do
    echo -n "."
    sleep 3   
  done
  echo ""
}

function setup-replicas() {
  MASTER_PODS=$(kubectl get pod | grep svr-0 | awk '{print $1}')

  for POD in $MASTER_PODS; do
    echo "Setup replica set for ${POD}"
    kubectl exec $POD -- mongosh /scripts/setup-replica.js --quiet
    OK=$(kubectl exec $POD -- mongosh --eval "rs.status().ok" --quiet)
    echo -n "Wait replicas are ok"
    until [[ $OK = 1 ]]; do
      OK=$(kubectl exec $POD -- mongosh --eval "rs.status().ok" --quiet)
      sleep 3
      echo -n "."
    done  
    echo ""
  done
}

function setup-router() {
  echo "Setup router"
  sleep 10
  POD=$(kubectl get pod | grep router | awk '{print $1}')
  kubectl exec $POD -- mongosh /scripts/setup-router.js --quiet
}

function main() {
  if [[ $1 = "cleanup" ]]; then 
    cleanup
  fi
  generate-shards
  deploy
  wait-pod-running
  setup-replicas
  setup-router
}

main $1
