#!/usr/bin/env bash

protoc -I protos/ protos/accounts.proto --python_out=app/domain/accounts