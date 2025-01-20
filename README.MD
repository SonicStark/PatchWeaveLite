# PatchWeaveTranslator

Learn patch analysis techniques from PatchWeave :)



## Base Env

Review setup steps of base env in [Dockerfile](./doc/Dockerfile).

<details><summary><b>apt</b></summary>

```bash
apt-get update && apt-get install -y \
    autoconf \
    apt-transport-https \
    bison \
    ca-certificates \
    cmake \
    curl \
    flex \
    git \
    google-perftools \
    libboost-all-dev \
    libgoogle-perftools-dev \
    libncurses5-dev \
    minisat \
    nano \
    ninja \
    perl \
    python \
    python-pip \
    software-properties-common \
    subversion \
    unzip \
    zlib1g-dev \
    wget
```

</details>

<details><summary><b>pip</b></summary>

```bash
/usr/bin/pip install --upgrade pip && pip install \
    pysmt \
    six \
    wllvm
```

</details>

<details><summary><b>/z3</b></summary>

```bash
git clone https://github.com/Z3Prover/z3.git /z3;

cd /z3
git checkout z3-4.8.1
python scripts/mk_make.py

cd /z3/build
make -j32 install

export PYTHONPATH="/z3/build/python"
echo "Y" | pysmt-install --z3
```

</details>

<details><summary><b>/stp</b></summary>

```bash
mkdir /stp
git clone https://github.com/stp/stp.git /stp/source
mkdir /stp/build

cd /stp/build
cmake ../source/
make -j32 install
```

</details>

<details><summary><b>/bear</b></summary>

```bash
mkdir /bear
git clone https://github.com/rizsotto/Bear.git /bear/source

cd /bear/source
git checkout 2.2.1
mkdir /bear/build

cd /bear/build
cmake ../source
make -j32 install
```

</details>

<details><summary><b>/radamsa</b></summary>

```bash
git clone https://gitlab.com/akihe/radamsa.git /radamsa

cd /radamsa
git checkout 30770f6e
make install
```

</details>

<details><summary><b>PatchWeave Tools with CLANG+LLVM 7.0 (/llvm/llvm-7)</b></summary>

```bash
wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key| apt-key add -
apt-add-repository "deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-7 main"
apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y  --no-install-recommends --force-yes \
    clang-7


mkdir -p /llvm/llvm-7
git clone http://llvm.org/git/llvm.git /llvm/llvm-7/source
cd /llvm/llvm-7/source
git checkout release_70

svn co https://llvm.org/svn/llvm-project/cfe/tags/RELEASE_700/final/       /llvm/llvm-7/source/tools/clang
svn co http://llvm.org/svn/llvm-project/compiler-rt/tags/RELEASE_700/final /llvm/llvm-7/source/projects/compiler-rt

git clone https://github.com/llvm-mirror/clang-tools-extra.git /llvm/llvm-7/source/tools/clang/tools/clang-extra
cd /llvm/llvm-7/source/tools/clang/tools/clang-extra
git checkout release_70

git clone https://github.com/rshariffdeen/clang-tools.git /llvm/llvm-7/source/tools/clang/tools/clang-tools

echo "add_clang_subdirectory(clang-tools)" >> /llvm/llvm-7/source/tools/clang/tools/CMakeLists.txt
echo "add_clang_subdirectory(clang-extra)" >> /llvm/llvm-7/source/tools/clang/tools/CMakeLists.txt

mkdir /llvm/llvm-7/build
cd    /llvm/llvm-7/build
cmake /llvm/llvm-7/source -DCMAKE_C_COMPILER=clang-7 -DCMAKE_CXX_COMPILER=clang++-7 \
                          -DCMAKE_BUILD_TYPE=Release \
                          -DCMAKE_ENABLE_ASSERTIONS=OFF \
                          -DLLVM_ENABLE_WERROR=OFF \
                          -DLLVM_TARGETS_TO_BUILD=X86 \
                          -DCMAKE_CXX_FLAGS="-std=c++11"

make -j32 install
```

</details>

<details><summary><b>PatchWeave KLEE with LLVM 3.4 (/llvm/llvm-34 & /klee)</b></summary>

```bash
mkdir -p /llvm/llvm-34

svn co http://llvm.org/svn/llvm-project/llvm/tags/RELEASE_34/final         /llvm/llvm-34/source
svn co http://llvm.org/svn/llvm-project/cfe/tags/RELEASE_34/final          /llvm/llvm-34/source/tools/clang
svn co http://llvm.org/svn/llvm-project/compiler-rt/tags/RELEASE_34/final  /llvm/llvm-34/source/projects/compiler-rt

mkdir /llvm/llvm-34/build
cd    /llvm/llvm-34/build
cmake /llvm/llvm-34/source -DCMAKE_C_COMPILER=clang-7 -DCMAKE_CXX_COMPILER=clang++-7 \
                           -DCMAKE_BUILD_TYPE=Release \
                           -DCMAKE_ENABLE_ASSERTIONS=OFF \
                           -DLLVM_ENABLE_WERROR=OFF \
                           -DLLVM_TARGETS_TO_BUILD=X86 \
                           -DCMAKE_CXX_FLAGS="-std=c++11"

make -j32 install

mkdir /klee

git clone https://github.com/klee/klee-uclibc.git /klee/uclibc
cd /klee/uclibc
./configure --make-llvm-lib
make -j32

curl -OL https://github.com/google/googletest/archive/release-1.7.0.zip
mv release-1.7.0.zip /klee/test.zip
cd /klee
unzip test.zip

git clone https://github.com/rshariffdeen/klee.git /klee/source
cd /klee/source
git checkout seedmode-external-calls

mkdir /klee/build
cd    /klee/build  
cmake /klee/source -DLLVM_CONFIG_BINARY=/llvm/llvm-34/build/bin/llvm-config \
                   -DCMAKE_CXX_FLAGS="-fno-rtti" \
                   -DENABLE_SOLVER_STP=ON \
                   -DENABLE_POSIX_RUNTIME=ON \
                   -DENABLE_KLEE_UCLIBC=ON \
                   -DKLEE_UCLIBC_PATH=/klee/uclibc \
                   -DGTEST_SRC_DIR=/klee/test \
                   -DENABLE_SYSTEM_TESTS=OFF \
                   -DENABLE_UNIT_TESTS=OFF
make -j32 install
```

</details>

<b>PatchWeave</b>

```bash
git clone https://github.com/rshariffdeen/PatchWeave.git /patchweave
```



## Workflow

Launch with config `openjpeg-to-jasper.conf`:
```
path_a:/data/openjpeg-jasper/div-zero-1/openjpeg-1.5.1
path_b:/data/openjpeg-jasper/div-zero-1/openjpeg-1.5.2
path_c:/data/openjpeg-jasper/div-zero-1/jasper-1.900.2
exploit_command_a:/applications/codec/j2k_to_image -i $POC -o out.bmp
exploit_command_c:/src/appl/imginfo -f $POC
path_poc:/data/exploits/jasper/CVE-2016-8691.j2k
asan_flag:integer
```

### 1ST - Initialize

```bash
# DIRECTORY_LOG
mkdir -p $(pwd)/logs
# DIRECTORY_TMP
mkdir -p $(pwd)/tmp
# DIRECTORY_BACKUP
mkdir -p $(pwd)/backup
# DIRECTORY_OUTPUT_BASE
mkdir -p $(pwd)/output
# DIRECTORY_OUTPUT
mkdir -p ${DIRECTORY_OUTPUT_BASE}/openjpeg-to-jasper

cp -r \
  /data/openjpeg-jasper/div-zero-1/jasper-1.900.2 \
  /data/openjpeg-jasper/div-zero-1/jasper-1.900.2-patch

mkdir -p ${DIRECTORY_OUTPUT}/fuzz-input
mkdir -p ${DIRECTORY_OUTPUT}/fuzz-output

export PYTHONPATH="/z3/build/python"
```

### 2ND - Exploit


### 3RD - Analyse


### 4TH - Trace


### 5TH - Concolic


### 6TH - Slice


### 7TH - Weave


### 8TH - Verify


### 9TH - Emitter
