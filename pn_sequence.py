import itertools
import collections


def pn_seq(seq):
    # R1
    r1 = 0
    for i in range(len(seq)):
        if seq[i] == 1:
            r1 += 1
        else:
            r1 -= 1
    if abs(r1) > 1:
        return False

    # R2
    runs = collections.defaultdict(int)
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

    num_runs = len(runs.keys())
    for i in range(1, num_runs):
        n = num_runs // (2**i)
        if n < 1:
            break
        if runs[i] < n:
            return False

    # R3
    correlation = []
    for t in range(len(seq)):
        c = 0
        for i in range(len(seq)):
            n1 = 2 * seq[i] - 1
            n2 = 2 * seq[(i + t) % len(seq)] - 1
            c += n1 * n2
        correlation.append(c)
    correlation = set(correlation)
    if len(correlation) > 2 or len(seq) not in correlation:
        return False
    print(correlation)
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
for i in range(len(init_seqs)):
    for j in range(len(taps)):
        output = lfsr(init_seqs[i], taps[j])
        if output is not None:
            seqs.append(output)

print('Number of sequence produce by LFSR: {}'.format(len(seqs)))

n = 0
output_file = open('output.txt', 'w')
for s in seqs:
    if pn_seq(s):
        print(s)
        n += 1
        output_file.write(''.join(str(b) for b in s) + '\n')
print('Number of pn-sequence: {}'.format(n))
