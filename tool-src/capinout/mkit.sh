#g++ mypty2.cpp -o capinout -static-libstdc++ -static-libgcc
g++ mypty2.cpp -o capinout -static
strip capinout
cp capinout ../../scripts/labtainer-student/lab_sys/sbin/

