# Info

Tool to find similar snippets in files.

Supposed to be ran as CI quality check to prevent copy-paste between files.

# Usage

As local program:

```
git clone ...
python3 main.py /path/to/code
```

As docker container:

```
docker run --rm -ti -v $(pwd):/code agrrh/similarity
docker run --rm -ti -v $(pwd):/code agrrh/similarity similarity /code/my/sub/dir
```

# Configuration

Configuration is possible with `.similarity.yml` in current directory:

```
---

# Skip settings
skip:
  paths:  # Paths and files
    - .git/
    - LICENSE.md
  types:  # File types (extensions)
    - bin
    - dat

# Snippet parser settings
snippet:
  lines_min: 3  # snippets not less than X lines

similarity:
  identical: true  # set to true to include actually identical snippets
  ratio_fail: 95
  topk: 3  # how many top similars to display if check not failed
```
