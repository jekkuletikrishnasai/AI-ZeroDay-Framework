#include <iostream>
#include <cstring>
#include <vector>
#include <cstdio>

extern "C" {
    void process_data(const char* input, size_t len) {
        char buffer[16];

        // BUG 1: Logic/Admin Access
        if (len > 10 && strncmp(input, "ADMIN_ACCESS", 12) == 0) {
            std::cout << "[BUG_FOUND] ID:01 | TYPE: Privilege Leak | LOC: AdminCheck" << std::endl;
            std::cout << "[SECRET] AWS_KEY=AKIA_PROD_SERVER_001" << std::endl;
        }

        // BUG 4 & 5: Buffer Overflows (Simulated to prevent fuzzer exit)
        if (len > 30) {
            if (input[20] == 'X') { 
                std::cout << "[BUG_FOUND] ID:04 | TYPE: Buffer Overflow | LOC: strcpy_input" << std::endl;
            } 
            if (input[25] == 'Y') { 
                std::cout << "[BUG_FOUND] ID:05 | TYPE: Stack Corruption | LOC: strcpy_static" << std::endl;
            } 
        }

        // BUG 8: Null Dereference (Simulated)
        if (len == 1 && input[0] == '\0') { 
            std::cout << "[BUG_FOUND] ID:08 | TYPE: Null Dereference | LOC: PointerAssign" << std::endl;
        }

        // BUG 10: Format String
        if (strstr(input, "%s%s%s") != NULL) { 
            std::cout << "[BUG_FOUND] ID:10 | TYPE: Format String Injection | LOC: printf_input" << std::endl;
        }
    }
}