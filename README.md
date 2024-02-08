============================================================================
# Vox Exporter Blender Addon for MagicaVoxel and VoxEdit
============================================================================

Vox Exporter is a Blender addon that exports any mesh into vox format for MagicaVoxel and VoxEdit

Unlock the creative potential of your Blender 3D designs by seamlessly and instantly exporting them from Blender to the popular VOX format, compatible with MagicaVoxel and VoxEdit. Introducing the Blender to VOX Exporter, a powerful and intuitive addon that simplifies the process of exporting your intricate Blender creations into a format perfect for voxel-based art.

This addon is powered by the free, open-source and multi-platform voxel editor Vengi Voxel more info at https://github.com/vengi-voxel/vengi

============================================================================
# Building vengi-voxconvert.exe on Windows 11
============================================================================

* Install CMake from https://cmake.org/download/
* Win+R > type "sysdm.cpl" > Advanced > Environment Variables...
* Click "New" and add path: C:/Program Files (x86)/GnuWin32/bin
* Download ninja.exe from https://ninja-build.org/
* Add ninja.exe to PATH or if you're lazy paste it into C:/Program Files (x86)/GnuWin32/bin
* Install VSCode from https://code.visualstudio.com/
* Download Visual Studio Community from https://visualstudio.microsoft.com/vs/community/
* You need to add at least 2 Workloads before installation: "MSVC" & "C++ Address Sanitizer"
* Navigate find the C/C++ compiler "cl.exe" somehwere in C:/Program Files/Microsoft Visual Studio/<year>/Community/VC/Tools/MSVC/<version>/bin/Hostx64/x64/cl.exe and copy this path
* Example: C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.38.33130/bin/Hostx64/x64/cl.exe
* Copy the path in the folder address bar and add 3 more environment variables CC and CMAKE_C_COMPILER and CMAKE_CXX_COMPILER with this path value.
* Then add just the directory (without cl.exe) into the PATH environment variable
* Open Visual Studio Community > Skip Sign-In > Skip this for Now
* Restart computer
* Windows > Search > "x64" > open: x64 Native Tools Command Prompt for VS 2022
* cd to the vengi folder and make sure you delete the "build" folder
* Open Makefile and change "ON" to "OFF" in -DUSE_SANITIZERS=OFF
* Type "make" to configure and build or build specific targets like "make voxedit" or "make voxconvert"

============================================================================
# SOME LINKS AND INFO
============================================================================

Bug: https://github.com/actions/runner-images/issues/8891 regarding clang_rt.asan_static_runtime_thunk-x86_64.lib

PowerShell ISE: Get-ChildItem -Path "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC" -Name

Download LLVM from https://github.com/llvm/llvm-project/releases/

https://devblogs.microsoft.com/cppblog/addresssanitizer-asan-for-windows-with-msvc/

ERROR: The code execution cannot proceed because clang_rt.asan_dynamic-x86_64.dll was not found. Reinstalling the program may fix this problem.