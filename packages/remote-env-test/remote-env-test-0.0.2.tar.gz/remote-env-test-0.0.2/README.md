# Goal:
Generate protobuf files in python and C++ to be used for remote access to RL environment.

**Supported version:**
* protoc 3.12.2
* grpc 1.30.0

# To build python API
```python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. ./env.proto```


## To build C++ API
```/bigdisk/lax/rl/grpc/.local/bin/protoc -I=. --cpp_out=. --grpc_out=. --plugin=protoc-gen-grpc=$(which grpc_cpp_plugin) ./env.proto```

```mv ./env.pb.h grpc_client/include/```

```mv ./env.pb.cc grpc_client/src/```     
    
```mv ./env.grpc.pb.h grpc_client/include/```
        
```mv ./env.grpc.pb.cc grpc_client/ ```

# How to use?
Run server.py to start a gym server on nvidia05 and then you can either use client.py 
or client.cpp to make calls to the server.

**Example**: start a server on nvidia05:
/bigdisk/lax/renaza/projects/anaconda3/bin/python server.py--host 10.122.32.31 --port 10020

Note: this particular python package satisfies the required packages, that is why we suggest testers to use it until we create a grpc package.