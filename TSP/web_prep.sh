#!/bin/bash
source ../.env/bin/activate
python node_modules/keras-js/encoder.py save/tsp_model.h5
