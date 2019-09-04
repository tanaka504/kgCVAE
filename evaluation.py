import os, re
import pickle
import argparse

target_pattern = re.compile(r'^Target \((.*?)\) >> (.*?)$')
sample_pattern = re.compile(r'^Sample 0 \((.*?)\) >> (.*?)$')
score_pattern = re.compile(r'^Avg recall (.*?$)')

parser = argparse.ArgumentParser()
parser.add_argument('--expr', default='kgCVAE')
args = parser.parse_args()

def parse(result):
    context = []
    for line in result:
        if line.split(' ')[0] == 'Src':
            context.append(line.split(': ')[1])
        if target_pattern.match(line):
            da_true = target_pattern.search(line).group(1)
            ref = target_pattern.search(line).group(2)
        if sample_pattern.match(line):
            print(line)
            da_pred = sample_pattern.search(line).group(1)
            hyp = sample_pattern.search(line).group(2)
    try:
        return {'DA_preds': da_pred,
                'DA_trues': da_true,
                'hyp': hyp,
                'ref': ref,
                'context': context}
    except:
        print(result)
        input()

def main():
    with open(os.path.join('./working/', args.expr, 'test.txt'), 'r') as f:
        data = f.read()
    results = data.split('\n\n')[:-1]
    consequence = [parse(result.split('\n')) for result in results]
    with open('../DA_conv/data/images/results_{}.pkl'.format(args.expr), 'wb') as f:
        pickle.dump(consequence, f)
    

if __name__ == '__main__':
    main()
