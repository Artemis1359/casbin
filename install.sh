#!/bin/bash

set -e

APP_NAME="my-fastapi-app"
POSTGRES_IMAGE="postgres:15"
ISTIO_VERSION="1.26.1" # Поменять на версию Istio, которую вы используете

echo "🚀 Запуск Minikube..."
minikube delete
minikube status > /dev/null 2>&1 || minikube start --memory=8192 --cpus=4
istioctl install --set profile=demo -y
# enable ingress gateway and istio

# echo "📄 Создание ключей..."
# openssl genrsa -out private_key.pem 2048
# openssl rsa -in private_key.pem -pubout -out public_key.pem
# mv private_key.pem public_key.pem app/api/

echo "📦 Сборка Docker-образа $APP_NAME..."
eval $(minikube docker-env)
docker build -t $APP_NAME:latest .

# minikube image load $APP_NAME:latest

echo "Добавление postgres-secret"

kubectl delete secret postgres-secret --ignore-not-found

kubectl create secret generic postgres-secret \
  --from-literal=username=prototype \
  --from-literal=password=prototype

echo "📥 Загрузка PostgreSQL-образа $POSTGRES_IMAGE..."
docker pull $POSTGRES_IMAGE
echo "Загрузка в k8s"
minikube image load $POSTGRES_IMAGE

echo "📄 Применение K8s-манифестов..."

kubectl label namespace default istio-injection=enabled --overwrite

kubectl apply -f infra/base/postgres-pvc.yaml
kubectl apply -f infra/base/postgres-deployment.yaml
kubectl apply -f infra/base/postgres-service.yaml
kubectl apply -f infra/base/fastapi-deployment.yaml
kubectl apply -f infra/base/fastapi-service.yaml

echo "📄 Применение Istio-манифестов..."

kubectl apply -f infra/istio/fastapi-gateway.yaml
kubectl apply -f infra/istio/fastapi-virtualservice.yaml
kubectl apply -f infra/istio/RequestAuthentication.yaml
kubectl apply -f infra/istio/AuthorizationPolicy.yaml

echo "⏳ Ожидание запуска pod'ов..."
kubectl wait --for=condition=Ready pod -l app=fastapi-app --timeout=120s || echo "⚠️ FastAPI pod не стал Ready"
kubectl wait --for=condition=Ready pod -l app=postgres --timeout=120s || echo "⚠️ PostgreSQL pod не стал Ready"

FASTAPI_POD=$(kubectl get pods -l app=fastapi-app -o jsonpath='{.items[0].metadata.name}')

# Проверка что он существует
if [ -n "$FASTAPI_POD" ]; then
  echo "✅ Пробрасываем порт 8000 с pod/$FASTAPI_POD..."
  kubectl port-forward pod/$FASTAPI_POD 8000:8000
else
  echo "❌ Не удалось найти под fastapi-app"
fi



