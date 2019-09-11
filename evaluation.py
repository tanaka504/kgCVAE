import os, re, json
import pickle
import argparse

target_pattern = re.compile(r'^Target \((.*?)\) >> (.*?)$')
sample_pattern = re.compile(r'^Sample \d \((.*?)\) >> (.*?)$')
score_pattern = re.compile(r'^Avg recall (.*?$)')

parser = argparse.ArgumentParser()
parser.add_argument('--expr', default='kgCVAE')
args = parser.parse_args()

def parse(result, refs):
    context = []
    hyps = []
    da_preds = []
    for line in result:
        if line.split(' ')[0] == 'Src':
            context.append(line.split(': ')[1])
        if target_pattern.match(line):
            da_true = target_pattern.search(line).group(1)
            ref = target_pattern.search(line).group(2)
        if sample_pattern.match(line):
            # print(line)
            da_pred = sample_pattern.search(line).group(1)
            hyp = sample_pattern.search(line).group(2)
            da_preds.append(da_pred)
            hyps.append(hyp)
    # assert len(context) == len(refs['context']), {'txt': context, 'json': refs['context']}
    try:
        return {'DA_preds': da_preds,
                'DA_trues': refs['resp_dialog_acts'],
                'hyps': hyps,
                'refs': refs['responses'],
                'context': context}
    except:
        print(result)
        input()

def main():
    with open(os.path.join('./working/', args.expr, 'test.txt'), 'r') as f:
        data = f.read()
    results = data.split('\n\n')[:-1]
    jsondata = json.load(open('./data/test_multi_ref.json', 'r'))
    assert len(jsondata) == len(results), '{} & {}'.format(len(jsondata), len(results))
    consequence = [parse(result.split('\n'), ref) for result, ref in zip(results, jsondata)]
    with open(os.path.join('./working/', 'result_{}.pkl'.format(args.expr)), 'wb') as f:
        pickle.dump(consequence, f)
    

if __name__ == '__main__':
    main()
