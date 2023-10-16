import Metal
import ctypes

# Load the Metal kernel. Kernel adds 2 to input, in-place.
dev = Metal.MTLCreateSystemDefaultDevice()  # Get GPU
src = open('add2.metal').read()  # Load the kernel source code
lib, _ = dev.newLibraryWithSource_options_error_(src, None, None)
func = lib.newFunctionWithName_("add2_kernel")

# Create input buffer. Initialized to all zeros.
storage = Metal.MTLResourceStorageModeShared
input_buffer = dev.newBufferWithLength_options_(1, storage)

# Define a 'command' that specifies how to run the kernel
commandQueue = dev.newCommandQueue()  # queue of commands
commandBuffer = commandQueue.commandBuffer()
computeEncoder = commandBuffer.computeCommandEncoder()  # start
pso = dev.newComputePipelineStateWithFunction_error_(func, None)[0]
computeEncoder.setComputePipelineState_(pso)  # set kernel to call
computeEncoder.setBuffer_offset_atIndex_(input_buffer, 0, 0) # arg1
grd = grp = Metal.MTLSizeMake(1, 1, 1)  # 1 thread globally
computeEncoder.dispatchThreads_threadsPerThreadgroup_(grd, grp)
computeEncoder.endEncoding()  # end

# Execute the 'command' we defined above
commandBuffer.commit()
commandBuffer.waitUntilCompleted()

# Check output. Input was 0, kernel adds 2, so output is 2.
buffer = input_buffer.contents().as_buffer(1)  # get buffer
item = ctypes.c_uint8.from_buffer(buffer)  # cast to uint8
assert item.value == 2, f"❌ Output does not match reference!"
print("✅ Reference matches output!")