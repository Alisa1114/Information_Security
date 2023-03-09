import itertools

def lfsr(init_seq, taps=[0, 3]):
  tmp = init_seq.copy()
  output_seq = tmp.copy()
  for i in range(15-4):
    output = 0
    for t in taps:
        output += tmp[t]
    output %= 2
    tmp = tmp[1:]
    tmp.append(output)
    output_seq.append(output)
    
    if tmp == init_seq:
      return None
  
  return output_seq

init_seqs = [list(seq) for seq in itertools.product([0,1], repeat=4)]
init_seqs.remove([0,0,0,0])
print(init_seqs)