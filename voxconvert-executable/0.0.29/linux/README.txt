Release Notes: https://github.com/vengi-voxel/vengi/releases

====================================================
INSTALLATION: EXECUTE EACH LINE IN ORDER
====================================================

sudo dpkg -i vengi-shared_0.0.31.0-1_amd64.deb
sudo dpkg -i vengi-voxconvert_0.0.31.0-1_amd64.deb
sudo apt-get install -f
vengi-voxconvert --version

====================================================
EXAMPLE EXECUTION AND OUTPUT
====================================================

[a@User]:/mnt/c/Users/harry/Downloads $ sudo dpkg -i vengi-shared_0.0.28.0-1_amd64.deb
Selecting previously unselected package vengi-shared.
(Reading database ... 33970 files and directories currently installed.)
Preparing to unpack vengi-shared_0.0.28.0-1_amd64.deb ...
Unpacking vengi-shared (0.0.28.0-1) ...
Setting up vengi-shared (0.0.28.0-1) ...
Processing triggers for shared-mime-info (2.1-2) ...
[a@User]:/mnt/c/Users/harry/Downloads $ sudo dpkg -i vengi-voxconvert_0.0.28.0-1_amd64.deb
Selecting previously unselected package vengi-voxconvert.
(Reading database ... 34024 files and directories currently installed.)
Preparing to unpack vengi-voxconvert_0.0.28.0-1_amd64.deb ...
Unpacking vengi-voxconvert (0.0.28.0-1) ...
dpkg: dependency problems prevent configuration of vengi-voxconvert:
 vengi-voxconvert depends on liblua5.4-0 (>= 5.4.4); however:
  Package liblua5.4-0 is not installed.

dpkg: error processing package vengi-voxconvert (--install):
 dependency problems - leaving unconfigured
Processing triggers for man-db (2.10.2-1) ...
Errors were encountered while processing:
 vengi-voxconvert
[a@User]:/mnt/c/Users/harry/Downloads $ sudo apt-get install -f
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Correcting dependencies... Done
The following additional packages will be installed:
  liblua5.4-0
The following NEW packages will be installed:
  liblua5.4-0
0 upgraded, 1 newly installed, 0 to remove and 46 not upgraded.
1 not fully installed or removed.
Need to get 152 kB of archives.
After this operation, 549 kB of additional disk space will be used.
Do you want to continue? [Y/n] y
Get:1 http://archive.ubuntu.com/ubuntu jammy/universe amd64 liblua5.4-0 amd64 5.4.4-1 [152 kB]
Fetched 152 kB in 2s (88.3 kB/s)
Selecting previously unselected package liblua5.4-0:amd64.
(Reading database ... 34057 files and directories currently installed.)
Preparing to unpack .../liblua5.4-0_5.4.4-1_amd64.deb ...
Unpacking liblua5.4-0:amd64 (5.4.4-1) ...
Setting up liblua5.4-0:amd64 (5.4.4-1) ...
Setting up vengi-voxconvert (0.0.28.0-1) ...
Processing triggers for libc-bin (2.35-0ubuntu3.1) ...
/sbin/ldconfig.real: /usr/lib/wsl/lib/libcuda.so.1 is not a symbolic link

[a@User]:/mnt/c/Users/harry/Downloads $ vengi-voxconvert --version
INFO: (0) voxconvert 0.0.28.0
[a@User]:/mnt/c/Users/harry/Downloads $