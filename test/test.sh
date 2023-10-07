#!/bin/bash

set -ex

curl -X GET 'http://localhost:5000/tg_msgs_raw?page=1&per_page=10'
