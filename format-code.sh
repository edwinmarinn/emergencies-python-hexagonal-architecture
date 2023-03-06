# Script to source code
RED='\033[0;31m'
NO_COLOR='\033[0m' # No Color

echo "Black src"
black ./src

echo "Black tests"
black ./tests

echo "Isort src"
isort ./src

echo "Isort tests"
isort ./tests
