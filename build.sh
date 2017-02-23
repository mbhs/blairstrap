#!/bin/bash

mp scss/* bootstrap/scss/
cd bootstrap
grunt dist
mv dist ..
