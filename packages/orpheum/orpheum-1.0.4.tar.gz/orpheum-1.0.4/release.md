# Releasing a new version of orpheum


These are adapted from the khmer release docs, originally written by
Michael Crusoe.

Remember to update release numbers/RC in:

* this document

## Testing a release


 1\. The below should be done in a clean checkout:
```
cd $(mktemp -d)
git clone https://github.com/czbiohub/orpheum.git
cd orpheum
```
2\. Set your new version number and release candidate (you might want to check https://github.com/czbiohub/orpheum/releases for next version number):
```
new_version=1.0.0
rc=rc1
```
 and then tag the release candidate with the new version number prefixed by
   the letter 'v':
```
git tag -a v${new_version}${rc}
git push --tags https://github.com/czbiohub/orpheum.git
```
3\. Test the release candidate. Bonus: repeat on Mac OS X:
```
cd ..
python3 -m venv testenv1
python3 -m venv testenv2
python3 -m venv testenv3
python3 -m venv testenv4

# First we test the tag

cd testenv1
source bin/activate
git clone --depth 1 --branch v${new_version}${rc} https://github.com/czbiohub/orpheum.git
cd orpheum
pip install -r requirements.txt
make test

# Secondly we test via pip

cd ../../testenv2
deactivate
source bin/activate
pip install -U setuptools
pip install -e "git+https://github.com/czbiohub/orpheum.git@v${new_version}${rc}#egg=orpheum[test]"
cd src/orpheum
make test
make dist
cp dist/orpheum*tar.gz ../../../testenv3/

# Is the distribution in testenv2 complete enough to build another
# functional distribution?

cd ../../../testenv3/
deactivate
source bin/activate
pip install -U setuptools
pip install orpheum*tar.gz
pip install pytest
tar xzf orpheum-${new_version}${rc}.tar.gz
cd orpheum-${new_version}${rc}
pip install -r requirements.txt
make dist
make test
```

4\. Publish the new release on the testing PyPI server.  You will need
   to change your PyPI credentials as documented here:
   https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives
   We will be using `twine` to upload the package to TestPyPI and verify
   everything works before sending it to PyPI:

```
pip install twine
twine upload --repository-url https://test.pypi.org/legacy/ dist/orpheum-${new_version}${rc}.tar.gz
```
   Test the PyPI release in a new virtualenv:
```
cd ../../testenv4
deactivate
source bin/activate
pip install -U setuptools
# install as much as possible from non-test server!
pip install sbiopython click httmock khmer networkx numpy pandas scikit-learn seaborn sourmash tqdm ipykernel joblib notebook pyarrow s3fs fastparquet
pip install -i https://test.pypi.org/simple --pre orpheum
orpheum info  # should print "orpheum version ${new_version}${rc}"
```
5\. Do any final testing:

   * check documentation

## How to make a final release

When you've got a thoroughly tested release candidate, cut a release like
so:

1. Create the final tag. Write the changes from previous version in the tag commit message. `git log --oneline` can be useful here, because it can be used to compare the two versions (and hopefully we used descriptive PR names and commit messages). An example comparing `2.2.0` to `2.1.0`:
`git log --oneline v2.1.0..v2.2.0`

```
cd ../orpheum
git tag -a v${new_version}
```
2. Publish the new release on PyPI (requires an authorized account).
```
make dist
twine upload dist/orpheum-${new_version}.tar.gz
```
3. Delete the release candidate tag and push the tag updates to GitHub:
```
git tag -d v${new_version}${rc}
git push --tags https://github.com/czbiohub/orpheum.git
git push --delete https://github.com/czbiohub/orpheum.git v${new_version}${rc}
```
4. Add the release on GitHub, using the tag you just pushed.  Name it 'version X.Y.Z'

## Bioconda - Not currently supported yet

The BiocondaBot has an `autobump` feature that should pick up new releases from PyPI, and open a PR in Bioconda. Review any changes
(especially dependency versions, since these don't get picked up).

This is an example PR: https://github.com/bioconda/bioconda-recipes/pull/17113

## Announce it - Not currently doing this yet

If a bioinformatics software is released and no one tweets, is it really released?

Examples:
https://twitter.com/luizirber/status/1108846466502520832

## To test on a blank Ubuntu system, may have to sudo

```
apt-cache update && apt-get -y install python-dev libfreetype6-dev && libbz2-dev && libcurl4-openssl-dev && libssl-dev && \
pip install orpheum[test]
```
