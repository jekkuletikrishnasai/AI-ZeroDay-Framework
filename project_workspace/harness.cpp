#include <unistd.h>  // Required for read() and ssize_t
#include <stddef.h>  // Required for size_t
#include <iostream>

// Link to the logic in core_logic.cpp
extern "C" {
    void process_data(const char* input, size_t len);
}

int main(int argc, char** argv) {
    unsigned char buf[1024];

    // __AFL_LOOP is the Persistent Mode macro for high-speed auditing
    while (__AFL_LOOP(1000)) {
        // Read from stdin (AFL++ sends data here)
        ssize_t len = read(0, buf, sizeof(buf));
        
        if (len > 0) {
            process_data((const char*)buf, (size_t)len);
        }
    }

    return 0;
}