# Voxelity Pro: Voxel File Format Exchange

Voxelity Pro: Voxel File Format Exchange is a comprehensive Blender addon designed to revolutionize your voxel-based workflows. With its intuitive features and seamless integration, it empowers artists and designers to unleash their creativity and explore new dimensions of voxel modeling within the familiar Blender environment.

Voxelity Pro supports seamless import and export of various popular textured voxel file formats, including MagicaVoxel.vox Qubicle.qb Voxlap.vxl and a plethora of many more voxel file formats, ensuring compatibility with a wide range of voxel editors and game engines. Additionally, this addon introduces an integrated voxelization feature for textured meshes, allowing for streamlined voxelization directly within Blender.

Documentation: https://blendermarket.com/products/voxelity-pro-voxel-file-format-exchange/docs

Powered by vengi-voxconvert, a cutting-edge voxel conversion tool developed by Martin Gerhardy as part of Vengi Voxel (https://github.com/vengi-voxel/vengi) — an open-source and multi-platform voxel editor — Voxelity Pro brings unparalleled voxel conversion capabilities directly to Blender, enhancing your workflow and expanding your creative possibilities.

# Building vengi-voxconvert.exe on Windows 11

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

# Some Links & Info


* Documentaion Debugging VSCode & Blender: https://github.com/hkunz/blender-addon-template
* Bug: https://github.com/actions/runner-images/issues/8891 regarding clang_rt.asan_static_runtime_thunk-x86_64.lib
* PowerShell ISE: Get-ChildItem -Path "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC" -Name
* Download LLVM from https://github.com/llvm/llvm-project/releases/
* https://devblogs.microsoft.com/cppblog/addresssanitizer-asan-for-windows-with-msvc/
* Bleeding Edge vengi-voxconvert: https://github.com/vengi-voxel/vengi/actions/workflows/main.yml
