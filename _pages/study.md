---
title: "Study"
permalink: /study/
author_profile: true
---

### <a href="https://ocw.mit.edu/courses/mathematics/18-175-theory-of-probability-spring-2014/lecture-slides/" target="_break">MIT OCW: Theory of Probability

<style>
    code {
        font-size: .75rem;
    }
</style>

```c
  #include<stdio.h>
  int main() {
    printf("Hello, I'm Jae. Welcome to my github page!");
  }
  ```

## Bash

> `$ echo -e "-e allows\nescaping characters"`

```
-e allows
escaping characters
```

> `$ cat -n test.txt`\
ㄴ `-n`  enumerates each line

> `$ bash .../target.sh`\
ㄴ runs inexecutable script

## Gits

* `git log -n3 code.py` shows the last 3 commits within `code.py`
* `git show [commit-identifier]` shows the details of the commit
* `git revert [commit-identifier]` undoes the changes made in the commit
    > in case of the immediate amending, use `git commit --amend`
* `git revert HEAD` undoes the most recent commit
* `git checkout [commit-id] [file-name]` also handles erroneous commits
* `git blame code.py`
    > Sometimes you have to find someone to be blamed(but not seriously) for bugs or errors.