# Introduction to CUDA

## Table of Contents

1. [What is CUDA?](#what-is-cuda)
2. [Installation and Setup](#installation-and-setup)
3. [GPU Architecture](#gpu-architecture)
4. [Memory Model](#memory-model)
5. [Kernel Basics](#kernel-basics)
6. [Thread Indexing](#thread-indexing)
7. [Memory Management](#memory-management)
8. [CUDA with Python](#cuda-with-python)
9. [Synchronization](#synchronization)
10. [Performance Optimization](#performance-optimization)
11. [Common Patterns](#common-patterns)
12. [Practice Exercises](#practice-exercises)
13. [Summary](#summary)

---

## What is CUDA?

CUDA (Compute Unified Device Architecture) is NVIDIA's parallel computing platform and programming model. It allows developers to use NVIDIA GPUs for general-purpose computation (GPGPU), achieving massive parallelism for data-intensive tasks.

Key concepts:
- **Host**: The CPU and its memory (system RAM)
- **Device**: The GPU and its memory (VRAM)
- **Kernel**: A function that runs on the GPU, executed by thousands of threads in parallel
- **SIMT**: Single Instruction, Multiple Threads -- NVIDIA's execution model where groups of threads execute the same instruction simultaneously
- **Heterogeneous computing**: CPU handles serial/control logic, GPU handles parallel data processing

Common applications:
- Deep learning training and inference
- Scientific simulations (molecular dynamics, fluid dynamics)
- Image and signal processing
- Cryptography and financial modeling
- Ray tracing and real-time rendering

---

## Installation and Setup

```bash
# Check if NVIDIA driver is installed
nvidia-smi

# Install CUDA Toolkit (Ubuntu example)
# Download from: https://developer.nvidia.com/cuda-downloads
# Or via package manager:
sudo apt install nvidia-cuda-toolkit

# Verify CUDA installation
nvcc --version

# Check available GPU properties
nvidia-smi -q | head -50
```

```cuda
// Verify CUDA works with a minimal program: deviceQuery.cu
#include <stdio.h>

int main() {
    int deviceCount = 0;
    cudaGetDeviceCount(&deviceCount);  // query number of GPUs

    for (int i = 0; i < deviceCount; i++) {
        cudaDeviceProp prop;
        cudaGetDeviceProperties(&prop, i);  // get properties for device i

        printf("Device %d: %s\n", i, prop.name);
        printf("  Compute Capability: %d.%d\n", prop.major, prop.minor);
        printf("  Total Global Memory: %.2f GB\n", prop.totalGlobalMem / 1e9);
        printf("  Multiprocessors: %d\n", prop.multiProcessorCount);
        printf("  Max Threads per Block: %d\n", prop.maxThreadsPerBlock);
        printf("  Warp Size: %d\n", prop.warpSize);
    }
    return 0;
}

// Compile and run:
// nvcc deviceQuery.cu -o deviceQuery && ./deviceQuery
```

---

## GPU Architecture

Understanding GPU hardware is essential for writing efficient CUDA code.

### Threads, Blocks, and Grids

```cuda
// CUDA organizes parallel execution in a hierarchy:
//
// Grid (entire kernel launch)
//   └── Block (a group of threads that share resources)
//         └── Thread (the smallest unit of execution)
//
// A kernel launch creates a grid of blocks.
// Each block contains up to 1024 threads.
// Threads within a block can cooperate via shared memory and synchronization.

// Example: 1D grid of 4 blocks, each with 256 threads = 1024 total threads
// <<<numBlocks, threadsPerBlock>>>
// <<<4, 256>>>
```

### Warps and Streaming Multiprocessors

```cuda
// A warp is a group of 32 threads that execute in lockstep on a single SM.
// All threads in a warp execute the same instruction at the same time.
// If threads in a warp diverge (different if/else paths), both paths are serialized.
//
// A Streaming Multiprocessor (SM) is the core processing unit on the GPU.
// Each SM can run multiple warps concurrently, switching between them to hide latency.
//
// SM resources (shared memory, registers) are divided among active blocks.
// More blocks per SM = higher occupancy = better latency hiding.
//
// Key hardware limits (vary by architecture):
//   - Max threads per block: 1024
//   - Max blocks per SM: depends on architecture (typically 16-32)
//   - Warp size: 32 (fixed across all NVIDIA GPUs)
//   - Max warps per SM: typically 48-64
```

When a kernel launches, the runtime distributes blocks to SMs, which divide them into warps. Warps are scheduled with zero-cost context switching to hide memory latency. Blocks execute independently in any order; threads within a block can synchronize with `__syncthreads()`.

---

## Memory Model

```cuda
// GPU memory hierarchy (from fastest to slowest):
//
// Registers      -- per-thread, fastest, limited (typically 255 per thread)
// Shared Memory  -- per-block, ~100x faster than global, user-managed cache
// L1/L2 Cache    -- automatic hardware caches
// Global Memory  -- accessible by all threads, high bandwidth but high latency
// Constant Memory -- read-only, cached, 64KB limit, broadcast to all threads
// Local Memory   -- per-thread overflow from registers, stored in global memory

// --- Shared memory (declared with __shared__) ---
__global__ void sharedMemExample(float* input, float* output, int n) {
    __shared__ float tile[256];  // shared among all threads in this block

    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        tile[threadIdx.x] = input[idx];  // load from global to shared
    }
    __syncthreads();  // wait for all threads to finish loading

    // Now all threads can read any element in tile[]
    if (idx < n) {
        // Example: access neighbor's data (requires shared memory)
        int neighbor = (threadIdx.x + 1) % blockDim.x;
        output[idx] = tile[threadIdx.x] + tile[neighbor];
    }
}

// --- Constant memory (declared with __constant__) ---
__constant__ float filter[64];  // 64KB max, read-only on device

// Set constant memory from the host
// cudaMemcpyToSymbol(filter, hostFilter, 64 * sizeof(float));

// --- Global memory ---
// Allocated with cudaMalloc, accessed by all threads
// Highest bandwidth but highest latency (~400-800 cycles)
```

---

## Kernel Basics

```cuda
// A kernel is a function that runs on the GPU
// Declare with __global__ qualifier, returns void

// Simple kernel: add two arrays element-wise
__global__ void vectorAdd(float* a, float* b, float* c, int n) {
    // Each thread computes one element
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (idx < n) {           // bounds check for when n isn't a multiple of blockDim
        c[idx] = a[idx] + b[idx];
    }
}

int main() {
    int n = 1000000;
    size_t bytes = n * sizeof(float);

    // Allocate host memory
    float *h_a = (float*)malloc(bytes);
    float *h_b = (float*)malloc(bytes);
    float *h_c = (float*)malloc(bytes);

    // Initialize host data
    for (int i = 0; i < n; i++) {
        h_a[i] = 1.0f;
        h_b[i] = 2.0f;
    }

    // Allocate device memory
    float *d_a, *d_b, *d_c;
    cudaMalloc(&d_a, bytes);
    cudaMalloc(&d_b, bytes);
    cudaMalloc(&d_c, bytes);

    // Copy data from host to device
    cudaMemcpy(d_a, h_a, bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b, bytes, cudaMemcpyHostToDevice);

    // Launch the kernel with <<<numBlocks, threadsPerBlock>>>
    int threadsPerBlock = 256;
    int numBlocks = (n + threadsPerBlock - 1) / threadsPerBlock;  // ceiling division
    vectorAdd<<<numBlocks, threadsPerBlock>>>(d_a, d_b, d_c, n);

    // Copy result back to host
    cudaMemcpy(h_c, d_c, bytes, cudaMemcpyDeviceToHost);

    // Verify result
    printf("c[0] = %.1f (expected 3.0)\n", h_c[0]);

    // Free memory
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);
    free(h_a);
    free(h_b);
    free(h_c);

    return 0;
}
```

Function qualifiers: `__global__` (host-callable kernel), `__device__` (device-only helper), `__host__` (host-only, default), `__host__ __device__` (compiles for both).

---

## Thread Indexing

```cuda
// CUDA provides built-in variables for thread identification:
//   threadIdx.x, .y, .z  -- thread index within a block
//   blockIdx.x, .y, .z   -- block index within the grid
//   blockDim.x, .y, .z   -- number of threads per block (in each dimension)
//   gridDim.x, .y, .z    -- number of blocks in the grid (in each dimension)

// --- 1D indexing (most common) ---
__global__ void kernel1D(float* data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    // idx gives a unique global thread ID across the entire grid
    if (idx < n) {
        data[idx] *= 2.0f;
    }
}

// --- 2D indexing (useful for images and matrices) ---
__global__ void kernel2D(float* matrix, int width, int height) {
    int col = blockIdx.x * blockDim.x + threadIdx.x;  // column index
    int row = blockIdx.y * blockDim.y + threadIdx.y;  // row index

    if (col < width && row < height) {
        int idx = row * width + col;  // convert 2D to 1D (row-major)
        matrix[idx] += 1.0f;
    }
}

// Launch a 2D kernel with 2D block and grid dimensions
// dim3 threadsPerBlock(16, 16);     // 16x16 = 256 threads per block
// dim3 numBlocks(
//     (width + 15) / 16,            // ceiling division for columns
//     (height + 15) / 16            // ceiling division for rows
// );
// kernel2D<<<numBlocks, threadsPerBlock>>>(d_matrix, width, height);

// --- Grid-stride loop (handle data larger than grid) ---
__global__ void gridStrideLoop(float* data, int n) {
    // Each thread processes multiple elements, striding by total grid size
    int stride = blockDim.x * gridDim.x;
    for (int idx = blockIdx.x * blockDim.x + threadIdx.x; idx < n; idx += stride) {
        data[idx] = data[idx] * 2.0f + 1.0f;
    }
}
// This pattern is preferred for production code: works for any data size,
// and the grid size can be tuned for occupancy independently of the data.
```

---

## Memory Management

```cuda
// Core memory management functions

// --- cudaMalloc: allocate device memory ---
float* d_data;
cudaMalloc(&d_data, n * sizeof(float));  // allocate n floats on GPU

// --- cudaMemcpy: transfer data between host and device ---
// Directions: cudaMemcpyHostToDevice, cudaMemcpyDeviceToHost, cudaMemcpyDeviceToDevice
cudaMemcpy(d_data, h_data, n * sizeof(float), cudaMemcpyHostToDevice);  // host -> device
cudaMemcpy(h_data, d_data, n * sizeof(float), cudaMemcpyDeviceToHost);  // device -> host

// --- cudaFree: release device memory ---
cudaFree(d_data);

// --- cudaMemset: initialize device memory ---
cudaMemset(d_data, 0, n * sizeof(float));  // zero out device memory

// --- Unified Memory (CUDA 6+): single address space for host and device ---
float* unified;
cudaMallocManaged(&unified, n * sizeof(float));  // accessible from both CPU and GPU
// CPU and GPU can both read/write; must cudaDeviceSynchronize() before host reads GPU results
cudaFree(unified);

// --- Pinned (page-locked) host memory for faster transfers ---
float* h_pinned;
cudaMallocHost(&h_pinned, n * sizeof(float));  // pinned host memory
// Pinned memory enables faster cudaMemcpy and is required for async transfers
cudaFreeHost(h_pinned);  // free pinned memory (not regular free())
```

```cuda
// --- Error checking macro (always use in production code) ---
#define CUDA_CHECK(call)                                                \
    do {                                                                \
        cudaError_t err = call;                                         \
        if (err != cudaSuccess) {                                       \
            fprintf(stderr, "CUDA error at %s:%d: %s\n",               \
                    __FILE__, __LINE__, cudaGetErrorString(err));        \
            exit(EXIT_FAILURE);                                         \
        }                                                               \
    } while (0)

// Usage:
// CUDA_CHECK(cudaMalloc(&d_data, bytes));
// CUDA_CHECK(cudaMemcpy(d_data, h_data, bytes, cudaMemcpyHostToDevice));
```

---

## CUDA with Python

### PyCUDA

```python
# PyCUDA: write raw CUDA kernels and call them from Python
# pip install pycuda

import pycuda.autoinit           # auto-initialize CUDA context
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import numpy as np

# Write a CUDA kernel as a string
mod = SourceModule("""
__global__ void multiply(float *a, float *b, float *c, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        c[idx] = a[idx] * b[idx];  // element-wise multiply
    }
}
""")

# Get the kernel function
multiply = mod.get_function("multiply")

# Prepare data
n = 1000
a = np.random.randn(n).astype(np.float32)
b = np.random.randn(n).astype(np.float32)
c = np.empty_like(a)

# Launch the kernel (PyCUDA handles memory transfers for numpy arrays)
multiply(
    cuda.In(a), cuda.In(b), cuda.Out(c), np.int32(n),
    block=(256, 1, 1),
    grid=((n + 255) // 256, 1)
)

print(f"Result sample: {c[:5]}")
print(f"Matches numpy: {np.allclose(c, a * b)}")
```

### Numba CUDA

```python
# Numba CUDA: write GPU kernels in pure Python syntax
# pip install numba

from numba import cuda
import numpy as np
import math

# Define a CUDA kernel using the @cuda.jit decorator
@cuda.jit
def vector_add(a, b, c):
    # Get global thread index
    idx = cuda.grid(1)  # shorthand for cuda.threadIdx.x + cuda.blockIdx.x * cuda.blockDim.x

    if idx < a.shape[0]:
        c[idx] = a[idx] + b[idx]  # each thread adds one element

# Prepare data
n = 1_000_000
a = np.ones(n, dtype=np.float32)
b = np.full(n, 2.0, dtype=np.float32)
c = np.zeros(n, dtype=np.float32)

# Transfer to GPU
d_a = cuda.to_device(a)
d_b = cuda.to_device(b)
d_c = cuda.device_array_like(c)  # allocate on GPU without copying

# Launch kernel
threads_per_block = 256
blocks_per_grid = math.ceil(n / threads_per_block)
vector_add[blocks_per_grid, threads_per_block](d_a, d_b, d_c)

# Copy result back
result = d_c.copy_to_host()
print(f"Sum check: {result[0]} (expected 3.0)")

# Numba device function (callable from kernels)
@cuda.jit(device=True)
def clamp(value, lo, hi):
    return max(lo, min(hi, value))  # clamp value to [lo, hi]

@cuda.jit
def clamp_kernel(data, lo, hi):
    idx = cuda.grid(1)
    if idx < data.shape[0]:
        data[idx] = clamp(data[idx], lo, hi)
```

### CuPy

```python
# CuPy: NumPy-compatible GPU array library (drop-in replacement)
# pip install cupy-cuda12x  (match your CUDA version)

import cupy as cp
import numpy as np

# Create GPU arrays (same API as NumPy)
a_gpu = cp.array([1.0, 2.0, 3.0, 4.0, 5.0])
b_gpu = cp.ones(5)

# Operations run on GPU automatically
c_gpu = a_gpu + b_gpu         # element-wise addition on GPU
d_gpu = cp.dot(a_gpu, b_gpu)  # dot product on GPU
e_gpu = cp.linalg.norm(a_gpu) # norm on GPU

# Convert back to NumPy when needed
c_cpu = cp.asnumpy(c_gpu)     # GPU -> CPU transfer
# Or: c_cpu = c_gpu.get()

# Large-scale example: matrix multiply
A = cp.random.randn(4096, 4096, dtype=cp.float32)
B = cp.random.randn(4096, 4096, dtype=cp.float32)
C = cp.matmul(A, B)  # fast GPU matrix multiplication

# CuPy also supports custom CUDA kernels via cp.RawKernel for low-level control
```

---

## Synchronization

```cuda
// --- __syncthreads(): barrier within a block ---
// All threads in a block must reach this point before any can proceed
__global__ void syncExample(float* data, int n) {
    __shared__ float cache[256];

    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        cache[threadIdx.x] = data[idx];
    }
    __syncthreads();  // ensure all threads have written to cache

    // Now safe to read any element in cache
    if (idx < n && threadIdx.x > 0) {
        data[idx] = cache[threadIdx.x] - cache[threadIdx.x - 1];
    }
}

// --- Atomic operations: thread-safe global memory updates ---
// Needed when multiple threads write to the same memory location

__global__ void histogram(int* data, int* bins, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        atomicAdd(&bins[data[idx]], 1);  // safely increment bin count
    }
    // Without atomicAdd, concurrent writes would cause race conditions
}

// Other atomics: atomicSub, atomicMin, atomicMax, atomicExch, atomicCAS, atomicAnd/Or/Xor
// Host-side: cudaDeviceSynchronize() blocks until all GPU work completes
```

---

## Performance Optimization

### Coalesced Memory Access

```cuda
// Coalesced access: consecutive threads access consecutive memory addresses
// This allows the hardware to combine multiple memory requests into fewer transactions

// GOOD: coalesced -- threads read consecutive addresses
__global__ void coalesced(float* data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        float val = data[idx];  // thread 0 reads data[0], thread 1 reads data[1], etc.
    }
}

// BAD: strided -- threads skip elements, wastes memory bandwidth
__global__ void strided(float* data, int n, int stride) {
    int idx = (blockIdx.x * blockDim.x + threadIdx.x) * stride;
    if (idx < n) {
        float val = data[idx];  // thread 0 reads data[0], thread 1 reads data[stride], etc.
    }
}
// Rule: within a warp, thread i should access address base + i for best performance
```

### Shared Memory Tiling

```cuda
// Tiling: load a tile of global memory into shared memory, then operate on it
// Reduces global memory accesses by reusing data from fast shared memory

// Tiled matrix multiply (simplified for square matrices of size N)
#define TILE_SIZE 16

__global__ void matMulTiled(float* A, float* B, float* C, int N) {
    __shared__ float tileA[TILE_SIZE][TILE_SIZE];
    __shared__ float tileB[TILE_SIZE][TILE_SIZE];

    int row = blockIdx.y * TILE_SIZE + threadIdx.y;
    int col = blockIdx.x * TILE_SIZE + threadIdx.x;
    float sum = 0.0f;

    // Loop over tiles
    for (int t = 0; t < (N + TILE_SIZE - 1) / TILE_SIZE; t++) {
        // Load tile from A and B into shared memory
        if (row < N && (t * TILE_SIZE + threadIdx.x) < N)
            tileA[threadIdx.y][threadIdx.x] = A[row * N + t * TILE_SIZE + threadIdx.x];
        else
            tileA[threadIdx.y][threadIdx.x] = 0.0f;

        if (col < N && (t * TILE_SIZE + threadIdx.y) < N)
            tileB[threadIdx.y][threadIdx.x] = B[(t * TILE_SIZE + threadIdx.y) * N + col];
        else
            tileB[threadIdx.y][threadIdx.x] = 0.0f;

        __syncthreads();  // wait for tile to be fully loaded

        // Compute partial dot product from this tile
        for (int k = 0; k < TILE_SIZE; k++) {
            sum += tileA[threadIdx.y][k] * tileB[k][threadIdx.x];
        }

        __syncthreads();  // wait before loading next tile
    }

    if (row < N && col < N) {
        C[row * N + col] = sum;
    }
}
```

### Occupancy

Occupancy = active warps / maximum warps per SM. Higher occupancy helps hide memory latency. Factors that limit it: threads per block, registers per thread, and shared memory per block. Use `cudaOccupancyMaxPotentialBlockSize()` to find the optimal block size for a given kernel.

---

## Common Patterns

### Parallel Reduction

```cuda
// Reduction: combine all elements into a single value (sum, max, etc.)
// Tree-based approach within each block, then combine block results

__global__ void blockSum(float* input, float* output, int n) {
    __shared__ float sdata[256];

    int tid = threadIdx.x;
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // Load element into shared memory (or 0 if out of bounds)
    sdata[tid] = (idx < n) ? input[idx] : 0.0f;
    __syncthreads();

    // Tree-based reduction within the block
    for (int stride = blockDim.x / 2; stride > 0; stride >>= 1) {
        if (tid < stride) {
            sdata[tid] += sdata[tid + stride];  // add partner's value
        }
        __syncthreads();  // sync after each level
    }

    // Thread 0 writes the block's result
    if (tid == 0) {
        output[blockIdx.x] = sdata[0];
    }
}
// After kernel completes, output[] contains per-block sums.
// Reduce those on CPU, or launch another reduction kernel.
```

### Prefix Sum (Scan)

Inclusive scan transforms each element into the sum of all preceding elements plus itself (e.g., `[3, 1, 7, 0, 4] -> [3, 4, 11, 11, 15]`). Implement using shared memory with iterative doubling: at each step, each thread adds the value `stride` positions behind it. Use `__syncthreads()` between each doubling step.

### Matrix Multiply (Naive)

A naive matrix multiply assigns each thread to one output element, computing a dot product of a row from A and a column from B. Launch with 2D blocks (e.g., `dim3(16,16)`) and 2D grid. The tiled version above is significantly faster due to shared memory reuse.

---

## Practice Exercises

### Exercise 1: Vector Operations
Write CUDA kernels for element-wise vector operations.

```cuda
// 1. Write a kernel that computes c[i] = a[i] * b[i] + scalar
// 2. Handle arrays of arbitrary size using grid-stride loops
// 3. Add CUDA_CHECK error handling to all CUDA API calls
// 4. Time the kernel using cudaEvent and compare to CPU
```

### Exercise 2: Image Processing
Apply a blur filter to a 2D image using CUDA.

```cuda
// 1. Load an image into a 2D array (width x height)
// 2. Write a 2D kernel that computes the average of each pixel's 3x3 neighborhood
// 3. Use shared memory tiling to reduce global memory reads
// 4. Compare performance with and without shared memory
```

### Exercise 3: Python GPU Acceleration
Rewrite a NumPy computation using CuPy and Numba.

```python
# 1. Write a NumPy function that computes pairwise Euclidean distances
# 2. Port it to CuPy (drop-in replacement)
# 3. Port it to a Numba CUDA kernel
# 4. Benchmark all three: NumPy (CPU) vs CuPy vs Numba CUDA
```

---

## Summary

CUDA enables massive parallelism by mapping computations onto GPU hardware:
- **Threads, blocks, and grids** form the execution hierarchy; warps of 32 threads execute in lockstep
- **Memory hierarchy** ranges from fast registers and shared memory to high-bandwidth global memory
- **Kernels** are launched with `<<<blocks, threads>>>` syntax and use thread indexing for work distribution
- **Memory management** uses `cudaMalloc`, `cudaMemcpy`, `cudaFree`; unified memory simplifies the model
- **Python integration** via PyCUDA (raw kernels), Numba (Python syntax), and CuPy (NumPy drop-in)
- **Synchronization** with `__syncthreads()` (intra-block) and atomic operations (global)
- **Performance** depends on coalesced memory access, occupancy, and shared memory tiling
- **Common patterns** like reduction, scan, and tiled matrix multiply form the building blocks of GPU algorithms

---

## Next Steps

- Explore **CUDA streams** for overlapping computation with memory transfers
- Learn **cuBLAS** and **cuDNN** for optimized linear algebra and deep learning primitives
- Study **Thrust** -- a C++ template library for CUDA with STL-like algorithms
- Profile your code with **NVIDIA Nsight** and **nvprof** to find bottlenecks
- Investigate **multi-GPU programming** with CUDA-aware MPI or NCCL
- Try **cooperative groups** for flexible thread synchronization beyond blocks

---

## Additional Resources

- [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/)
- [CUDA Toolkit Documentation](https://developer.nvidia.com/cuda-toolkit)
- [CUDA By Example (book)](https://developer.nvidia.com/cuda-example)
- [Numba CUDA Documentation](https://numba.readthedocs.io/en/stable/cuda/)
- [CuPy Documentation](https://docs.cupy.dev/en/stable/)
- [PyCUDA Documentation](https://documen.tician.de/pycuda/)
- [NVIDIA Nsight Systems](https://developer.nvidia.com/nsight-systems)
