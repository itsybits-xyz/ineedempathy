#!/bin/bash

echo "Starting Feelings!"
for p in $(cat script/data/feelings.txt)
do
    curl -X POST "http://localhost:8000/cards" -H  "accept: application/json" -H "Content-Type: application/json" -d "{\"name\":\"$p\",\"type\":\"feeling\"}"
done

echo "Starting Needs!"
for p in $(cat script/data/needs.txt)
do
    curl -X POST "http://localhost:8000/cards" -H  "accept: application/json" -H "Content-Type: application/json" -d "{\"name\":\"$p\",\"type\":\"need\"}"
done
