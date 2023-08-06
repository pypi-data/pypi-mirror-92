#!/bin/bash


deps=/work/apps/teca-deps/
src=/home/bloring/work/teca/teca
testd=/home/bloring/work/teca/TECA_test

if [[ ! -d $deps ]]
then
    echo "dependencies not found"
    exit -1
fi
if [[ ! -d $src ]]
then
    echo "sources not found"
    exit -1
fi
if [[ ! -d $testd ]]
then
    echo "test dir not found"
    exit -1
fi

. $deps/bin/teca_env.sh

pushd .
mkdir -p $testd/mem_check
rm -rf $testd/mem_check/*
cd $testd/mem_check

cmake \
    -DCMAKE_BUILD_TYPE=Debug \
    -DBUILD_TESTING=ON \
    -DTECA_DATA_ROOT=/home/bloring/work/teca/teca/bin/../../TECA_data ../ \
    $src

ctest -D ExperimentalBuild
ctest --timeout 120 -D ExperimentalTest
ctest --timeout 120 -D ExperimentalMemCheck
ctest --timeout 120 -D ExperimentalSubmit

popd
