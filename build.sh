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
}

build()
{
    clean
    echo "Building..."
    source virtualenv/bin/activate && python setup.py sdist && python setup.py bdist_wheel
}

deploy()
{
    echo "Deploying..."
    twine upload dist/*
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