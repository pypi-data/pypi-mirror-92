# git refs

list git references(branches, tags) on local and remote repositories.

## Install

    pip3 install -U git-refs

## Example

```bash
$ git-refs
local branch master 5a4344acd93627b7e20d5c86aa18a587c90a17d9 -> origin/master
remote reference master 5a4344acd93627b7e20d5c86aa18a587c90a17d9 origin
```

### CSV output format

```bash
$ CSV=1 git-refs
where,type,name,sha,remote
local,branch,master,5a4344acd93627b7e20d5c86aa18a587c90a17d9,origin/master
remote,reference,master,5a4344acd93627b7e20d5c86aa18a587c90a17d9,origin
```

You can use [`printable`](https://github.com/weaming/printable) to view csv in terminal:

    CSV=1 git-refs | printable -t csv -f /dev/stdin
