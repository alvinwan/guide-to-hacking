/* import metal library, like `from metal import *` */
#include <metal_stdlib>
using namespace metal;

/**

Define a function called `add2_kernel` that doesn't return
a value. Instead, we modify the input array in-place.
   
:param in uint8_t*: An array of integers, as input.
:param id uint: The index of the current thread. We use this
    to index into the input array. In other words, we
    parallelize by assigning each thread to a different
    element of the input array.

*/
kernel void add2_kernel(device uint8_t *in  [[ buffer(0) ]],
                        uint id [[ thread_position_in_grid ]]) {
    in[id] = in[id] + 2;    /* add 2 in-place */
}