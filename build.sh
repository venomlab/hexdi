#!/usr/bin/env bash

test()
{
    echo "Run cases..."
    source virtualenv/bin/activate && python tests/test_main.py
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
    source virtualenv/bin/activate && python setup.py sdist && python setup.py bdist_wheel
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