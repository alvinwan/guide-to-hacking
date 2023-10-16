import Metal
import random

# Load the Metal kernel. Kernel adds 2 to input, in-place.
dev = Metal.MTLCreateSystemDefaultDevice()  # Get GPU
src = open('add2.metal').read()  # Load the kernel source code
lib, _ = dev.newLibraryWithSource_options_error_(src, None, None)
func = lib.newFunctionWithName_("add2_kernel")

# Create input buffer. Initialize to random integers.
storage = Metal.MTLResourceStorageModeShared
N = 1024  # our input will have 1024 integers
input_buffer = dev.newBufferWithLength_options_(N, storage)
input_contents = input_buffer.contents().as_buffer(N)
random_integers = [random.randint(0, 253) for _ in range(N)]
for i in range(N):  # copy random values into buffer
    input_contents[i] = random_integers[i]

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
output_python = [x + 2 for x in random_integers]
assert output_metal == output_python, f"❌ Output does not match reference!"
print("✅ Reference matches output!")
