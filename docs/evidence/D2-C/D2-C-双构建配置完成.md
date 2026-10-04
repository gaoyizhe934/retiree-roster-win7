# C 杞?D2 鍙屾瀯寤洪厤缃紙瀹屾垚璁板綍锛?
- 浜ゆ帴渚濇嵁锛歔寮€鍙戣鍒抅(../../閫€浼戜汉鍛樺悕鍐屾墦鍗板皬绋嬪簭寮€鍙戣鍒?docx) 绗?5 鑺?D2-C 鍗°€乕涓冮樁娈靛紑鍙戜换鍔℃竻鍗昡(../../../reference/涓冮樁娈靛紑鍙戜换鍔℃竻鍗?xlsx) 绗?A15 琛?- 瀹屾垚鏃ユ湡锛?026-10-05
- 鐘舵€侊細**COMPLETE锛堝€欓€夛級** 鈥斺€?鍙屾瀯寤洪厤缃笌绌虹▼搴忓€欓€夊寘宸插缓绔嬶紱姝ｅ紡 Gate 1 缁撹鐢遍潪浣滆€?R 缁欏嚭
- 鍩虹嚎渚濇嵁锛歔OD-0002](../../decisions/OD-0002-Windows7-SP1鐩爣鍩虹嚎.md)锛圵indows 7 SP1 / 6.1.7601 / x86/x64锛?
## 涓€銆佸畬鎴愬畾涔夊鐓?
| 瀹屾垚瀹氫箟 | 鐘舵€?| 璇佹嵁 |
| --- | --- | --- |
| `CMakeLists.txt`锛堟寮忔瀯寤轰笌鍙戝竷鍏ュ彛锛?| 瀹屾垚 | 浠撳簱鏍?`CMakeLists.txt`锛沎閰嶇疆瀵圭収](config-comparison.md) |
| `xmake.lua`锛堣緟鍔╅暅鍍忥級 | 瀹屾垚 | 浠撳簱鏍?`xmake.lua`锛沎閰嶇疆瀵圭収](config-comparison.md) |
| 涓ゅ鍙鐜板懡浠?| 瀹屾垚 | [cmake-configure.txt](cmake-configure.txt)銆乕xmake-configure.txt](xmake-configure.txt) |
| 閰嶇疆瀵圭収 | 瀹屾垚 | [config-comparison.md](config-comparison.md) |
| 渚濊禆妫€鏌ョ粨鏋?| 瀹屾垚 | [dumpbin-cmake-app.txt](dumpbin-cmake-app.txt)銆乕dumpbin-xmake-app.txt](dumpbin-xmake-app.txt) |
| CMake 鍊欓€夌┖绋嬪簭 | 瀹屾垚 | [cmake-install.txt](cmake-install.txt)銆乣dist/candidate/app.exe` |
| Win7 SP1 x86/x64 鍚姩璇佹嵁 | 瀹屾垚 | [x86-CMake鍊欓€夌┖绐楀彛.png](x86-CMake鍊欓€夌┖绐楀彛.png)銆乕x64-CMake鍊欓€夌┖绐楀彛.png](x64-CMake鍊欓€夌┖绐楀彛.png) |

## 浜屻€佸伐鍏烽摼锛坱oolchain-versions.txt锛?
- Visual Studio 2017 Build Tools 15.9锛歁SVC 14.16.27023锛坈l 19.16.27054锛夛紝骞冲彴宸ュ叿闆?`v141_xp`锛圵in32 涓?x64锛夛紝Windows 7.1A SDK銆?- CMake 3.15.7锛堟寮忓叆鍙ｏ級銆?- XMake 2.9.9锛堣緟鍔╅暅鍍忥級銆?- dumpbin 14.16.27054.0銆?
## 涓夈€佹瀯寤轰笌娴嬭瘯缁撴灉

| 娴佹按绾?| 缁撴灉 | 璇佹嵁 |
| --- | --- | --- |
| CMake 閰嶇疆 | 鎴愬姛锛宍PlatformToolset=v141_xp` | [cmake-configure.txt](cmake-configure.txt) |
| CMake 鏋勫缓 | 鎴愬姛锛沗app.exe`銆乣roster_sqlite.lib`銆? 涓祴璇?exe | [cmake-build.txt](cmake-build.txt) |
| CTest | 9/9 閫氳繃 | [ctest.txt](ctest.txt) |
| XMake 閰嶇疆 | VS2017 / MSVC 19.16.27054 | [xmake-configure.txt](xmake-configure.txt) |
| XMake 鏋勫缓 | 鎴愬姛 | [xmake-build.txt](xmake-build.txt) |
| XMake 娴嬭瘯 | `roster_tests` 鍏ㄩ儴閫氳繃 | [xmake-tests.txt](xmake-tests.txt) |

娴嬭瘯闆嗭細`build_config_test`锛堥攣瀹氬畯涓?`/MT` 鑷锛夈€乣sqlite_smoke_test`锛圫QLite 3.45.3 闈欐€侀摼鎺ヨ嚜妫€锛夈€佹棦鏈?7 涓绾︽秷璐硅€呫€?
## 鍥涖€佷骇鐗╀笌渚濊禆妫€鏌?
- `app.exe` 73,216 瀛楄妭锛涗緷璧栦粎 `USER32.dll`銆乣KERNEL32.dll`锛屾棤 MSVCR/UCRT 鈫?`/MT` 闈欐€佽繍琛屽簱纭锛圼dumpbin-cmake-app.txt](dumpbin-cmake-app.txt)銆乕dumpbin-xmake-app.txt](dumpbin-xmake-app.txt)锛夈€?- PE 澶达細machine x86 (14C)锛宭inker 14.16锛宻ubsystem 5.01锛圵indows GUI锛夛紙[dumpbin-cmake-app-headers.txt](dumpbin-cmake-app-headers.txt)锛夈€?- 鍊欓€夊寘甯冨眬锛歚app.exe` + `data/`銆乣templates/`銆乣backups/`銆乣exports/`銆乣logs/`銆乣docs/`锛圼cmake-install.txt](cmake-install.txt)锛夈€?
## 浜斻€乄in7 SP1 鍚姩璇佹嵁

- 涓绘満铏氭嫙鏈猴細`Win7RTM-SP1-x86`锛?.1.7601锛寈86锛夈€乣Win7RTM-SP1-x64`锛?.1.7601锛寈64锛夛紝鍧囨潵鑷?D1 `00_Base` 鍩虹嚎銆?- 浼犺緭鏂瑰紡锛氬彧璇?ISO锛坄roster-d2c.iso`锛屽嵎鏍?`ROSTER_D2C`锛夌粡 SATA 鍏夐┍閫佸叆 Guest锛屼笉瀹夎 Guest Additions銆佷笉姹℃煋鍩虹嚎銆?- 缁撴灉锛?2 浣?CMake 鍊欓€夊寘鍦ㄤ袱鍙?VM 鍧囧惎鍔ㄧ┖绐楀彛锛屾爣棰樻纭樉绀衡€滈€€浼戜汉鍛樺悕鍐屾墦鍗板皬绋嬪簭鈥濓紱x64 缁忕敱 WOW64 杩愯銆?- 杩愯鍚庡凡鎭㈠锛歺86 淇濆瓨鐘舵€侊紱x64 鍏虫満锛涘厜椹变笌绔彛鏁版仮澶嶅師鍊笺€?
## 鍏€佺涓夋柟渚濊禆

- 5 涓浐瀹氭簮鍖呭凡褰掓。浜庢湰鍦?`third_party/archives/`锛堜笉鍏ュ簱锛夛紝SHA-256 璁板綍瑙?[third_party/README.md](../../../third_party/README.md)銆?- SQLite 3.45.3 amalgamation 宸?vendored 鍒?`third_party/sqlite/` 骞剁撼鍏ヤ袱濂楁瀯寤猴紙`roster_sqlite`锛夈€?- xlsxio_read / Expat / zlib / libxlsxwriter 鍦ㄥ悇鑷娑堣垂鐨勪换鍔″崱锛圖3 瀵煎叆銆丏5 瀵煎嚭锛夌撼鍏ワ紝绾冲叆鍓嶄笉閾炬帴銆?
## 涓冦€佹敼鍔ㄦ枃浠?
```text
CMakeLists.txt                       姝ｅ紡鏋勫缓涓庡彂甯冨叆鍙?xmake.lua                            杈呭姪寮€鍙戦暅鍍?src/ui/main_win32.cpp                绌虹獥鍙ｅ€欓€夌▼搴忥紙B 杞?D2-B 灏嗘墿灞曚负鐣岄潰楠ㄦ灦锛?tests/build_config_test.cpp    鏋勫缓閰嶇疆鑷
tests/sqlite_smoke_test.cpp    SQLite 闈欐€侀摼鎺ヨ嚜妫€
third_party/README.md                渚濊禆褰掓。涓?SHA-256
third_party/sqlite/                  SQLite 3.45.3 amalgamation
packaging/package/                   鍊欓€夊寘鐩綍楠ㄦ灦
.gitignore                           鎺掗櫎绗笁鏂规簮鍖呭綊妗?```

## 鍏€佸凡鐭ヨ竟鐣屼笌寰呭姙

- xlsxio_read/Expat/zlib/libxlsxwriter 鏈帴鍏ワ細灞炰簬 D3/D5 娑堣垂渚濊禆锛屼笉鍦ㄦ湰鍗¤寖鍥淬€?- XMake 浣跨敤 v141 缂栬瘧鍣ㄤ絾涓嶅惎鐢?`v141_xp` 骞冲彴宸ュ叿闆嗭細瑙勫垝鏄庣‘ XMake 浠呬綔寮€鍙戞満蹇€熸瀯寤轰笌閰嶇疆涓€鑷存€у鏍革紝姝ｅ紡鍊欓€夊寘鍙敱 CMake 鐢熸垚銆?- `v141_xp` 鏋勫缓浜х敓 MSB8051 寮冪敤鎻愮ず锛圴S 閫氱敤鎻愮ず锛夛紝涓嶅奖鍝嶆瀯寤轰笌杩愯銆?- 鏈崱鍙瘉鏄庘€滅┖绋嬪簭鍚姩鈥濓紱瀵煎叆銆佺淮鎶ゃ€佺瓫閫夈€佸鍑轰笌 L2/L3 瀹屾暣閾捐矾灞炰簬鍚庣画鍗′笌 Gate銆?