#!/bin/sh
mypy .

echo "press to test..."
read

pytest
