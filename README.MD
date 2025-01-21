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

</br>

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

</br>

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

According to the building order, default version of LLVM toolchain would be seized by **3.4**.</br>

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

The marks:
 - `A`: /data/openjpeg-jasper/div-zero-1/openjpeg-1.5.1
 - `B`: /data/openjpeg-jasper/div-zero-1/openjpeg-1.5.2
 - `C`: /data/openjpeg-jasper/div-zero-1/jasper-1.900.2
 - `D`: /data/openjpeg-jasper/div-zero-1/jasper-1.900.2-patch

### 2ND - Exploit

```python
FILE_EXPLOIT_OUTPUT_A = DIRECTORY_OUTPUT + "/exploit-log-a"
FILE_EXPLOIT_OUTPUT_B = DIRECTORY_OUTPUT + "/exploit-log-b"
FILE_EXPLOIT_OUTPUT_C = DIRECTORY_OUTPUT + "/exploit-log-c"
FILE_EXPLOIT_OUTPUT_D = DIRECTORY_OUTPUT + "/exploit-log-d"
```

Build A, B, C, D with *Bear*:

```python
if Values.ASAN_FLAG == "":
    safe_exec(Builder.build_normal, "building binaries")
else:
    safe_exec(Builder.build_asan, "building binaries")
```

Run POC and collect info from stdout/stderr:

```python
safe_exec(test_exploits, "testing exploit case")
safe_exec(collect_exploit_info, "collecting exploit information")
```

### 3RD - Analyse

```python
FILE_DIFF_INFO_JSON = DIRECTORY_OUTPUT + "/diff_info.json"
```

#### Textural difference

```python
safe_exec(analyse_source_diff, "analysing source diff")
```

It will run *GNU diffutils* on source code tree firstly:
```python
# TODO: Include cases where a file is added or removed
diff_command = "diff -ENZBbwqr " + project_path_a + " " + project_path_b + " -X " + output_ext + "> " + output_diff_file + ";"
diff_command += "cat " + output_diff_file + "| grep -P '\.c and ' > " + output_c_diff + ";"
diff_command += "cat " + output_diff_file + "| grep -P '\.h and ' > " + output_h_diff
```

Then walk and diff each C/C++ source file with `A` as baseline index:
```python
diff_command = "diff -ENBZbwr " + file_a + " " + file_b + " > " + output_file
...
diff_loc = file_a + ":" + str(start_a)
diff_info[diff_loc] = dict()
diff_info[diff_loc]['operation'] = operation

if operation == 'insert':
    diff_info[diff_loc]['new-lines'] = (start_b, end_b)
    diff_info[diff_loc]['old-lines'] = (start_a, end_a)
elif operation == "delete":
    diff_info[diff_loc]['remove-lines'] = (start_a, end_a)
elif operation == "modify":
    diff_info[diff_loc]['old-lines'] = (start_a, end_a)
    diff_info[diff_loc]['new-lines'] = (start_b, end_b)
```

#### AST structural difference

> A textual difference between the two programs provides a list of diff locations in terms of source file paths and line numbers. 
> 
> We use information from the textual difference to identify potentially changed locations that are relevant for the patch and
> use this information to generate the AST in a granular level instead of generating AST for the complete program.

> Once we identified the necessary code chunks required for the patch, 
> we captured the modification as a transformation of an abstract syntax tree.
> *PatchWeave* constructs an AST for the function that contains the identified chunk in both *Pa* and *Pb*.
> 
> Using a tree difference algorithm [GumTree](https://github.com/GumTreeDiff/gumtree), 
> we generate a transformation script for the ASTs constructed earlier. 

```python
safe_exec(analyse_ast_diff, "analysing ast diff")
```

Actually it will run [crochet-diff](https://github.com/SonicStark/PatchWeaveTranslatorTools/tree/master/crochet-diff) on each item in `diff_info`, with the following steps equivalently:
```python
ASTGenerator.generate_ast_script(source_a, source_b, script_file_path, False)

ast_map_a = ASTGenerator.get_ast_json(source_path_a)
ast_map_b = ASTGenerator.get_ast_json(source_path_b)

ASTGenerator.generate_ast_script(source_a, source_b, script_file_path, True)

mapping_ba = dict()
with open(script_file_path, "r") as script_file:
    script_lines = script_file.readlines()
    for script_line in script_lines:
        if "Match" in script_line:
            node_id_a = int(((script_line.split(" to ")[0]).split("(")[1]).split(")")[0])
            node_id_b = int(((script_line.split(" to ")[1]).split("(")[1]).split(")")[0])
            mapping_ba[node_id_b] = node_id_a
```

Then the ast script is filtered and saved to each item, too:
```python
filtered_ast_script = list()

if diff_info[diff_loc]['operation'] == 'insert':
    start_line_b, end_line_b = diff_info[diff_loc]['new-lines']
    line_range_b = (start_line_b, end_line_b)
    line_range_a = (-1, -1)
    filtered_ast_script = Filter.filter_ast_script(ast_script,
                                                (source_path_a, line_range_a, ast_map_a),
                                                (source_path_b, line_range_b, ast_map_b),
                                                mapping_ba)
elif diff_info[diff_loc]['operation'] == 'modify':
    line_range_a = diff_info[diff_loc]['old-lines']
    line_range_b = diff_info[diff_loc]['new-lines']
    filtered_ast_script = Filter.filter_ast_script(ast_script,
                                                (source_path_a, line_range_a, ast_map_a),
                                                (source_path_b, line_range_b, ast_map_b),
                                                mapping_ba)
if filtered_ast_script is None:
    del diff_info[diff_loc]
    continue

diff_info[diff_loc]['ast-script'] = filtered_ast_script
```

### 4TH - Trace

Total 3 steps:
```python
safe_exec(Builder.build_llvm, "building llvm files")
safe_exec(trace_donor,        "tracing donor program")
safe_exec(trace_target,       "tracing target program")
```

#### Step 1: emit llvm

Build A, B, C, D with *wllvm*, *Clang 3.4*. Then use `extract-bc` from *wllvm* to get IR bitcode for KLEE.

#### Step 2: klee trace

Trace A, B, C with [a modified KLEE](https://github.com/rshariffdeen/klee/tree/seedmode-external-calls):
```python
trace_command = "cd " + binary_path + ";"
sym_args = "--posix-runtime --libc=uclibc --print-trace --print-stack -max-time=80 -max-memory=2048 "

trace_command += "klee " + sym_args + " " + binary_name + ".bc " \
            + exploit_command.replace("$POC", poc_path) + "  > " + log_path + " 2>&1"
```

The two new options of the modified KLEE are defined and used in `Executor.cpp`:
```c++
cl::opt<bool> PrintTrace("print-trace", cl::init(false),
        cl::desc("Output source location for each instruction executed (default=off)"));
cl::opt<bool> PrintStack("print-stack", cl::init(false),
        cl::desc("Output stack information on error exit (default=off)"));

void Executor::executeInstruction(ExecutionState &state, KInstruction *ki) {
    Instruction *i = ki->inst;
    std::string sourceLoc = ki->getSourceLocation();
    if (sourceLoc.find("klee") == std::string::npos){
        if (PrintTrace)
            errs() << "\n[trace] " << sourceLoc << " - " << ki->inst->getOpcode() << "\n";
        if (PrintLLVMInstr)
            errs() << "\n[LLVM] " << *(ki->inst) << "\n";
    }
    switch (i->getOpcode()) { ... }
}

void Executor::terminateStateOnError(ExecutionState &state,
                                     const llvm::Twine &messaget,
                                     enum TerminateReason termReason,
                                     const char *suffix,
                                     const llvm::Twine &info) {...
        if (PrintStack){
            errs() << "Stack: \n"; state.dumpStack(errs(), kmodule->targetData.get());
        } ...}
```

### 5TH - Concolic

Run so-called *sym_trace* on A, B and C:
```python
safe_exec(sym_trace_donor,  "generating symbolic trace information from donor program")
safe_exec(sym_trace_target, "generating symbolic trace information from target program")
```

For example it will launch [the modified KLEE](https://github.com/rshariffdeen/klee/tree/seedmode-external-calls) for B:
```python
trace_command = "cd " + binary_path + ";"

sym_args = "-print-path -write-smt2s --libc=uclibc --posix-runtime --external-calls=all --only-replay-seeds --seed-out=$KTEST -max-time=80 -max-memory=2048"

trace_command += "klee " + sym_args.replace("$KTEST", poc_path) + " " + binary_name + ".bc " \
                    + binary_arguments.replace("$POC", "A") + " --sym-files 1 " + str(bit_size) \
                    + "  > " + log_path + " 2>&1"

sym_file_path = binary_path + "/klee-last/test000001.smt2 "
```

Note that `-print-path` is implemented as
```c++
cl::opt<bool> PrintPath("print-path", cl::init(false),
        cl::desc("Output path condition along with source location as and when it's updated (default=off)"));

void Executor::addConstraint(ExecutionState &state, ref<Expr> condition) { ...
    if (!res) {
        state.addConstraint(condition);
        if(PrintPath) {
            std::string constraints;
            getConstraintLog(state, constraints, Interpreter::SMTLIB2);
            errs() << "\n[path:condition] " << state.pc->getSourceLocation() << " : " << constraints<< "\n";
        }
    } ... 
}

void Executor::terminateStateOnError(ExecutionState &state,
                                     const llvm::Twine &messaget,
                                     enum TerminateReason termReason,
                                     const char *suffix,
                                     const llvm::Twine &info) { ...
        if (usingSeeds && PrintPath){
            //interpreterHandler->processTestCase(state, msg.str().c_str(), suffix);
            exit(0);
        } ...
}
```

### 6TH - Slice

Total 3 steps:

```python
# step 1
# safe_exec(remove_code, "slicing code not in trace")

diff_info = Slicer.slice_code_from_trace(Values.diff_info, trace_list, path_a, path_b)
diff_info = Slicer.slice_ast_script(diff_info, Values.PATH_A, Values.PATH_B, trace_list)
Values.diff_info = Slicer.slice_skipped_diff_locs(diff_info)
```

```python
# step 2
# if not Values.BACKPORT:
#     safe_exec(remove_func_calls, "slicing function calls")

diff_info = Slicer.slice_function_calls(Values.diff_info, Concolic.sym_path_b.keys(), path_a, path_b)
diff_info = Slicer.slice_ast_script(diff_info, Values.PATH_A, Values.PATH_B, Trace.list_trace_b)
Values.diff_info = Slicer.slice_skipped_diff_locs(diff_info)
```

```python
# step 3
# safe_exec(remove_redundancy, "slicing redundant diff")

suspicious_lines = Exploit.donor_suspect_line_list
Values.diff_info = Slicer.slice_redundant_patches(Values.diff_info, suspicious_lines)
```

Default value of `Values.BACKPORT` is `False`, so this step makes <b><i>Slice</b></i> depends on <b><i>Concolic</b></i> different from what stated in paper...

### 7TH - Weave


### 8TH - Verify


### 9TH - Emitter
