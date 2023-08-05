import seissolxdmf as sx
for i in range(0,40):
   n= sx.ReadNElements('output_o5/tpvNorcia2d_fs_B_o5_16mio-fault.xdmf')
print(n)
