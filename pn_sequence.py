import itertools


def pn_seq(seq):
    # R1
    num1 = 0
    num0 = 0
    for i in range(len(seq)):
        if seq[i] == 1:
            num1 += 1
        else:
            num0 += 1
    if abs(num1 - num0) > 1:
        return False

    # R2
    runs = [0] * len(seq)
    previous = seq[0]
    length = 1
    for i in range(1, len(seq)):
        if previous != seq[i]:
            runs[length] += 1
            length = 1
            previous = seq[i]
        else:
            length += 1
    runs[length] += 1

    num_runs = sum(runs)
    # print(runs)

    for i in range(1, num_runs):
        n = num_runs / (2**i)
        if n < 1:
            break
        if runs[i] < n:
            return False

    # R3
    correlation = []
    shift_list = seq.copy()
    for t in range(len(seq)):
        c = 0
        for i in range(len(seq)):
            if seq[i] == shift_list[i]:
                c += 1
            else:
                c -= 1
        # 讓list往右shift一格
        shift_list.insert(0, shift_list.pop())
        correlation.append(c)
    correlation = set(correlation)
    if len(correlation) > 2 or len(seq) not in correlation:
        return False

    return True


def lfsr(init_seq, taps=[1, 0, 0, 1]):
    tmp = init_seq.copy()
    output_seq = tmp.copy()
    for i in range(15 - 4):
        output = 0
        for i in range(4):
            output += tmp[i] * taps[i]
        output %= 2
        tmp = tmp[1:]
        tmp.append(output)
        output_seq.append(output)

        if tmp == init_seq:
            return None

    return output_seq


# test
# seq = lfsr([0, 1, 1, 0], [1, 0, 0, 1])
# print('{} is pn-sequence: {}'.format(seq, pn_seq(seq)))

init_seqs = [list(seq) for seq in itertools.product([0, 1], repeat=4)]
init_seqs.remove([0, 0, 0, 0])
taps = init_seqs.copy()

seqs = []
init_bit_tap = []
for i in range(len(init_seqs)):
    for j in range(len(taps)):
        output = lfsr(init_seqs[i], taps[j])
        if output is not None:
            init_bit_tap.append([init_seqs[i], taps[j]])
            seqs.append(output)

print('Number of sequence produce by LFSR: {}'.format(len(seqs)))

n = 0
output_file = open('output.txt', 'w')
for i in range(len(seqs)):
    if pn_seq(seqs[i]):
        init_bit, tap = init_bit_tap[i]
        tap_idx = [i for i in range(len(tap)) if tap[i] == 1]
        print('init bits: {}'.format(init_bit))
        print('tap: {}'.format(tap_idx))
        print(seqs[i])
        n += 1
        output_file.write('init bits: {}\n'.format(''.join(
            str(b) for b in init_bit)))
        output_file.write('tap: {}\n'.format(','.join(str(t)
                                                      for t in tap_idx)))
        output_file.write('pn-seq: ' + ''.join(str(b)
                                               for b in seqs[i]) + '\n\n')
print('Number of pn-sequence: {}'.format(n))
output_file.close()
