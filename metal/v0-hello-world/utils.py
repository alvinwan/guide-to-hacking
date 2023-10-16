import Metal
import numpy as np


def load(path, function_name):
    # Load the Metal kernel into Python. Kernel computes log of input.
    device = Metal.MTLCreateSystemDefaultDevice()  # Get the default GPU device
    kernel_source = open(path).read()  # Load the kernel source code
    library = device.newLibraryWithSource_options_error_(kernel_source, None, None)[0]  # Load kernel into Python
    kernel_function = library.newFunctionWithName_(function_name)  # Access specific kernel function, which adds 2 to input, in-place
    pso = device.newComputePipelineStateWithFunction_error_(kernel_function, None)[0]  # Create pipeline that calls kernel

    def log(input_array):
        # Create input and output buffers. Initialize input to random floats.
        input_buffer = device.newBufferWithBytes_length_options_(input_array, input_array.nbytes, Metal.MTLResourceStorageModeShared)  # initialize input buffer from array
        output_buffer = device.newBufferWithLength_options_(input_array.nbytes, Metal.MTLResourceStorageModeShared)  # create empty output buffer

        # Define a 'command' that specifies how to run the kernel
        threads = Metal.MTLSizeMake(1024, 1, 1)  # 1024 thread per thread group
        groups = Metal.MTLSizeMake(32, 1, 1)  # 32 groups
        commandQueue = device.newCommandQueue()  # Create a command queue for kernel calls
        commandBuffer = commandQueue.commandBuffer()  # Create a command buffer to hold the command
        computeEncoder = commandBuffer.computeCommandEncoder()  # Start defining the command
        computeEncoder.setComputePipelineState_(pso)  # set the kernel we want to call
        computeEncoder.setBuffer_offset_atIndex_(input_buffer, 0, 0)  # Set the first argument to the kernel
        computeEncoder.setBuffer_offset_atIndex_(output_buffer, 0, 1)  # Set the second argument to the kernel
        computeEncoder.dispatchThreads_threadsPerThreadgroup_(threads, groups)  # Configure threads to run kernel
        computeEncoder.endEncoding()

        # Execute the 'command' we defined above
        commandBuffer.commit()
        commandBuffer.waitUntilCompleted()

        # Check the output is correct.
        output_contents = output_buffer.contents().as_buffer(input_array.nbytes)  # get buffer object we can modify
        output_array = np.frombuffer(output_contents, dtype=np.float32)  # reinterpret buffer as float32 array
        return output_array
    return log