#include <iostream>
#include <thread>
#include <chrono>

int main() {
    std::cout << "[*] Starting DNP3 Outstation..." << std::endl;

    // Simulated loop
    while (true) {
        std::cout << "[+] Responding to DNP3 Master (simulated)" << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(3));
    }

    return 0;
}
