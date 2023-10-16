from utils import load
import numpy as np

# create an array, with a single random float value
input_array = np.random.random(1).astype(np.float32)

# load kernel from file, as a runnable python function
log = load('log.metal', function_name='log_kernel')

# run kernel on input array above
output_array = log(input_array)

# check output is correct
error = np.abs(output_array - np.log(input_array)).max()
assert error < 1e-5, "❌ Output does not match reference!"
print("✅ Reference matches output!")