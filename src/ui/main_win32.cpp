// D2-C build skeleton: minimal Win32 empty window (formal CMake candidate).
// Track B owns the real UI skeleton (D2-B); this entry exists to prove the
// locked build/package pipeline (Win32, C++14, Unicode, /MT, 0x0601).
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

namespace {

const wchar_t kWindowClass[] = L"RetireeRosterMainWindow";
const wchar_t kWindowTitle[] = L"\u9000\u4f11\u4eba\u5458\u540d\u518c\u6253\u5370\u5c0f\u7a0b\u5e8f";

LRESULT CALLBACK WindowProc(HWND hwnd, UINT message, WPARAM wparam, LPARAM lparam) {
    switch (message) {
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;
        default:
            return DefWindowProcW(hwnd, message, wparam, lparam);
    }
}

}  // namespace

int WINAPI wWinMain(HINSTANCE instance, HINSTANCE previous, PWSTR command_line, int show_command) {
    static_cast<void>(previous);
    static_cast<void>(command_line);

    WNDCLASSEXW window_class = {};
    window_class.cbSize = sizeof(window_class);
    window_class.lpfnWndProc = WindowProc;
    window_class.hInstance = instance;
    window_class.lpszClassName = kWindowClass;
    window_class.hCursor = LoadCursorW(nullptr, IDC_ARROW);
    window_class.hbrBackground = reinterpret_cast<HBRUSH>(COLOR_WINDOW + 1);
    if (RegisterClassExW(&window_class) == 0) {
        return 1;
    }

    HWND window = CreateWindowExW(0, kWindowClass, kWindowTitle, WS_OVERLAPPEDWINDOW,
                                  CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,
                                  nullptr, nullptr, instance, nullptr);
    if (window == nullptr) {
        return 1;
    }

    ShowWindow(window, show_command);
    UpdateWindow(window);

    MSG message = {};
    while (GetMessageW(&message, nullptr, 0, 0) > 0) {
        TranslateMessage(&message);
        DispatchMessageW(&message);
    }
    return static_cast<int>(message.wParam);
}
