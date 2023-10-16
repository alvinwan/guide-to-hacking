import Metal
from math import log
import numpy as np

# Load the Metal kernel. Kernel logs input, in-place.
dev = Metal.MTLCreateSystemDefaultDevice()  # Get GPU
src = open('add2.metal').read()  # Load the kernel source code
lib, _ = dev.newLibraryWithSource_options_error_(src, None, None)
func = lib.newFunctionWithName_("add2_kernel")

# Create input buffer. Initialize to random floats.
storage = Metal.MTLResourceStorageModeShared
input_array = np.random.random(1024).astype(np.float32)
input_buffer = dev.newBufferWithBytes_length_options_(
    input_array, input_array.nbytes, storage)

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
output = input_buffer.contents().as_buffer(input_array.nbytes)
output_array = np.frombuffer(output, dtype=np.float32)
error = np.abs((input_array + 2.0) - output_array).max()
assert error < 1e-5, f"❌ Output does not match reference!"
print("✅ Reference matches output!")