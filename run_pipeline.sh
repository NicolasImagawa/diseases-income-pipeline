echo "Please insert the following values"

echo "1 - GCP project name"
read PROJECT_NAME
PROJECT="${PROJECT_NAME:-"diseases-and-income-us"}"
echo "Source project is: $PROJECT"
echo "---------------------------------------"


echo "2 - Dataset/schema name"
read DATASET_NAME
DATASET="${DATASET_NAME:-"main"}"
echo "Source dataset/schema is: $DATASET"
echo "---------------------------------------"

echo "3 - GCS Bucket name"
read BUCKET_NAME
BUCKET="${BUCKET_NAME:-"diseases-and-income-us-nimagawa"}"
echo "Source bucket is: $BUCKET"
echo "---------------------------------------"

python ./scripts/create_json.py \
--project=${PROJECT} \
--dataset=${DATASET} \
--bucket=${BUCKET}

python ./scripts/create_yml.py \
--project=${PROJECT} \
--dataset=${DATASET}

#Build the Docker image
docker build -t airflow_diseases_income:v001 .

# Start all Airflow services in detached mode
docker compose up -d

echo "Loading Airflow..."
sleep 75

echo "Please check the Airflow UI at https://localhost:8081"