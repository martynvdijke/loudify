# Runner

The runner job is to get the data from the broker and split the network packet into the I/Q data and the flowgraph variables.
The runner will call the flowgraph `cran_recieve.py` unfortunately the file generate from `gnuradio-companion` needs to be adapted in order for everything to work.

First the following import statements need to be appended to the top of the flowgraph.

```python
import pickle
import time
import codecs
```

Next the actual import statements the initialization function of the flowgraph needs to be adapted in the following way:

```python
    def __init__(self, flowgraph_vars):
        gr.top_block.__init__(self, "Cran reciever")
        self._lock = threading.RLock()

        ##################################################
        # Variables
        ##################################################
        self.bw = bw = flowgraph_vars['bw']
        self.time_wait = time_wait = 200
        self.sf = sf = flowgraph_vars['sf']
        self.samp_rate = samp_rate = flowgraph_vars['samp_rate']
        self.pay_len = pay_len = flowgraph_vars['pay_len']
        self.n_frame = n_frame = 2
        self.multi_control = multi_control = True
        self.impl_head = impl_head = flowgraph_vars['impl_head']
        self.has_crc = has_crc = flowgraph_vars['has_crc']
        self.frame_period = frame_period = 2
        self.cr = cr = flowgraph_vars['cr']
```

Finally, the last part that needs to be edited is the main function and the calling function and its needs to be edited in the following way.

```python
def main(flowgraph_vars,top_block_cls=cran_recieve, options=None):
    tb = top_block_cls(flowgraph_vars)
    tb.start()
    time.sleep(1)
    
    while True:
        num_messages = tb.blocks_message_debug_0.num_messages()
        if num_messages >= 1:
            tb.stop()
            exit(0)

if __name__ == '__main__':
    unpickled = pickle.loads(codecs.decode(sys.argv[1].encode(), "base64"))
    # input = pickle.load(sys.stdin.buffer)
    # print(input)
    main(unpickled)
```