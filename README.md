# SIBADI Competitions

## Development

### Linting

Python linters in this project are set up as [pre-commit](https://pre-commit.com/) hook. Do these steps to use them:
1. Install requirements
```
pip install -r requirements.txt
```

2. Initialize pre-commit hook
```
pre-commit install
```

3. Run linters
```
pre-commit run --all-files
```

When linters are set, they now will be trigered any time you do commit. If there are any errors detected before commit, fix them, then do `git add .` and commit once again.
