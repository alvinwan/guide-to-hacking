import Metal
import ctypes
import random
from math import log

# Load the Metal kernel. Kernel logs input, in-place.
dev = Metal.MTLCreateSystemDefaultDevice()  # Get GPU
src = open('add2.metal').read()  # Load the kernel source code
lib, _ = dev.newLibraryWithSource_options_error_(src, None, None)
func = lib.newFunctionWithName_("add2_kernel")

# Create input buffer. Initialize to random integers.
storage = Metal.MTLResourceStorageModeShared
N = 1024  # our input will have 1024 integers
B = N * 4  # fp32 is 4 bytes per value
input_buffer = dev.newBufferWithLength_options_(B, storage)
input_contents = input_buffer.contents().as_buffer(B)
input_array = (ctypes.c_float * N).from_buffer(input_contents)
input_list = [random.random() for _ in range(N)]  # generate
input_array[:] = input_list  # copy random values into buffer

# Define a 'command' that specifies how to run the kernel
commandQueue = dev.newCommandQueue()  # queue of commands
commandBuffer = commandQueue.commandBuffer()
computeEncoder = commandBuffer.computeCommandEncoder()  # start
pso = dev.newComputePipelineStateWithFunction_error_(func, None)[0]
computeEncoder.setComputePipelineState_(pso)  # set kernel to call
computeEncoder.setBuffer_offset_atIndex_(input_buffer, 0, 0) # arg1
grp = Metal.MTLSizeMake(32, 1, 1)  # 32 threads per group
grd = Metal.MTLSizeMake(1024, 1, 1)  # 1024 threads per grid
computeEncoder.dispatchThreads_threadsPerThreadgroup_(grd, grp)
computeEncoder.endEncoding()  # end

# Execute the 'command' we defined above
commandBuffer.commit()
commandBuffer.waitUntilCompleted()

# Check output. Input was 0, kernel adds 2, so output is 2.
output_metal = list(input_contents)
output_python = [x + 2 for x in input_list]
assert [(a - b) < 1e-5 for a, b in zip(output_metal, output_python)], f"❌ Output does not match reference!"
print("✅ Reference matches output!")