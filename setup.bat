python setup.py sdist bdist_wheel
twine upload dist/*
pip install gamecord --upgrade
pause