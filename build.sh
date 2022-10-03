#!/usr/bin/env bash

test()
{
    echo "Run cases..."
    tox
}

clean()
{
    echo "Cleaning..."
    rm -rf build/
    rm -rf dist/
    rm -rf *.egg-info/
    rm -f README.rst
}

build()
{
    clean
    echo "Building..."
    mdtorst
    python setup.py sdist && python setup.py bdist_wheel
}

deploy()
{
    echo "Deploying..."
    twine upload dist/*
}

mdtorst()
{
    pandoc --from=markdown --to=rst --output=README.rst README.md
}


while [ "$1" != "" ]; do
    case $1 in
        "test" ) test ;;
        "clean" ) clean ;;
        "build" ) build ;;
        "deploy" ) deploy ;;
    esac
    shift
done