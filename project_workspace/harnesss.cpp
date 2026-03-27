#include <stddef.h>
#include <stdint.h>
#include <string>

extern "C" void process_data(const char* input, size_t len);

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    if (Size == 0) return 0;
    // Call the function defined in your native_target.cpp
    process_data(reinterpret_cast<const char*>(Data), Size);
    return 0;
}