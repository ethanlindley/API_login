#!/bin/bash
cd ..
cd ..

rm -f ./libs/libz*

export DYLD_FRAMEWORK_PATH=Frameworks/
export DYLD_LIBRARY_PATH=libs/
chmod +x ./"The Legend of Pirates Online (BETA)"
./"The Legend of Pirates Online (BETA)"
