#include <metal_stdlib>
using namespace metal;

/**

Define a function called `log_kernel` that doesn't return
a value. Instead, we write results to an output array.
   
:param in float*: An array of floats, as input.
:param out float*: An array of floats, which will contain
    our output.
:param id uint: The index of the current thread. We use this
    to index into the input array. In other words, we
    parallelize by assigning each thread to a different
    element of the input array.

*/
kernel void log_kernel(device float *in  [[ buffer(0) ]],
                       device float *out [[ buffer(1) ]],
                       uint id [[ thread_position_in_grid ]]
) {
    out[id] = log(in[id]);  /* log each element *not in-place */
}