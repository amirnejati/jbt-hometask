[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)


1. unit-test
1. dockerize
1. flake


https://github.com/tweepy/tweepy
https://github.com/PyGithub/PyGithub


alembic revision -m "first migration" --autogenerate --head head
alembic upgrade head                                            

to set up the git hook scripts at .git/hooks/pre-commit:
pre-commit install

If you want to manually run all pre-commit hooks on a repository, run:
pre-commit run --all-files

To run individual hooks use:
pre-commit run <hook_id>

pre-commit can also be used as a tool for continuous integration.
To check only files which have changed, which may be faster, use:
pre-commit run --from-ref origin/HEAD --to-ref HEAD

pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-push

if you want to skip running the pre-commit hooks on commit or push you can do this by
 adding --no-verify to the git commit or git push commands.
