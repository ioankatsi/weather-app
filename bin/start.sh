# Go into the app root directory
SCRIPTPATH=$(pwd -P)
cd "$SCRIPTPATH/"

curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh

# Exit immediately if a command exits with a non-zero status
set -e

# Run Alembic migrations
cd app && alembic upgrade head

cd ..

# Ensure we have everything installed
pip3 install --upgrade pip && pip3 install -r requirements.txt

# Start the FastAPI server
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
