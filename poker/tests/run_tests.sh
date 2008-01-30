PYTHONPATH=../.. trace2html.py -o /tmp -w poker -r ./test_runner.py

if [ "$(uname)" == "Darwin" ]; then
    open /tmp/index.html
fi
