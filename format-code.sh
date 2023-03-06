# Script to format source code

echo "Black src"
black ./src

echo "Black tests"
black ./tests

echo "Isort src"
isort ./src

echo "Isort tests"
isort ./tests
