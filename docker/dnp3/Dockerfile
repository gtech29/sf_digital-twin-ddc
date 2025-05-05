# Use Ubuntu as base
FROM ubuntu:latest

# Install dependencies
RUN apt-get update && apt-get install -y \
    git cmake g++ python3 python3-pip libboost-all-dev libasio-dev

# Clone OpenDNP3 repo
RUN git clone https://github.com/dnp3/opendnp3.git /opendnp3

# Set working directory
WORKDIR /opendnp3

# Build OpenDNP3 (Linux-compatible)
RUN cmake -S . -B build && \
    cmake --build build -j$(nproc)

# Create a directory for your simulator
RUN mkdir -p /outstation
COPY simple_outstation.cpp /outstation/simple_outstation.cpp

# Build the outstation simulator (dummy for now)
WORKDIR /outstation
RUN g++ simple_outstation.cpp -o outstation \
    -std=c++17 \
    -I/opendnp3/cpp/libs/include \
    -I/opendnp3/third_party/asio/asio/include \
    -lboost_system -lpthread

# Default run command
CMD ["./outstation"]
