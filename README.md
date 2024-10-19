# Boids模擬鳥類群集行為規則

## 執行步驟 : 
1. 編譯C++使其成為dll

Windows:
```
    g++ -shared -o boids.dll boids.cpp -O2 -fopenmp -static-libgcc -static-libstdc++ -static -lpthread'
```

Mac:
```
    g++ -shared -o libboids.dylib boids.cpp -O2 -fopenmp -fPIC
```

2. 執行main.py
```
    python3 main.py
```