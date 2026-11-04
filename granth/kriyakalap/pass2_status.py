import json,os
b=json.load(open('pass2_batches.json'))
todo=[x for x in b if not all(os.path.exists(f'addenda/s{k}.md') for k in x['keys'])]
print(len(b)-len(todo),'/',len(b),'done; next:',[(x['id'],x['keys'][0],x['keys'][-1]) for x in todo[:8]])
