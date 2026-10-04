// D2-C: verifies that the formal build locks the agreed target configuration.
// The checks are compile-time so a misconfigured build fails instead of shipping.
#include <cstdio>

#if !defined(UNICODE) || !defined(_UNICODE)
#error "UNICODE/_UNICODE must be defined (Unicode builds only)"
#endif

#if !defined(WINVER) || WINVER != 0x0601
#error "WINVER must be 0x0601 (Windows 7 target)"
#endif

#if !defined(_WIN32_WINNT) || _WIN32_WINNT != 0x0601
#error "_WIN32_WINNT must be 0x0601 (Windows 7 target)"
#endif

#if defined(_DLL)
#error "the dynamic MSVC runtime (/MD) is forbidden; use /MT"
#endif

#if !defined(_MT)
#error "the static MSVC runtime (/MT) must be used"
#endif

#if defined(_MSVC_LANG)
#if _MSVC_LANG != 201402L
#error "MSVC must compile as C++14 (/std:c++14)"
#endif
#elif __cplusplus != 201402L
#error "the compiler must compile as C++14"
#endif

#if defined(_WIN64) || defined(_M_X64) || defined(_M_ARM64)
#error "the formal distribution is Win32/x86 only"
#endif

static_assert(sizeof(void*) == 4, "32-bit pointer size required");
static_assert(sizeof(wchar_t) == 2, "UTF-16 wchar_t required");

int main() {
    std::puts("build_config_test: PASS (Win32, C++14, Unicode, /MT, WINVER=0x0601)");
    return 0;
}
