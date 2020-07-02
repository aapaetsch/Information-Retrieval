[Assignment specs](https://sites.ualberta.ca/~denilson/cmput397-winter-2019-assignment-1.html)

# Don't Forget to

1. Submit the URL of your repository on eClass **as soon as you read this line**!
1. Disclose all sources you consult
1. Spend time on your design; you need to break down the tasks so that all team members can work in parallel
1. Meet with the TA about your group progress and to ask for advice
1. Test your code
1. Document any assumptions and design decisions
1. Add clear execution instructions

Our instructions to run are in the readme's for that portion.
To run our tests, run `chmod u+x tests.sh` from our top level directory, and then `./tests.sh`
The tests pass if all the messages indicate they pass.

Map reduce is not running with hadoop, but creates an index. It can run with hadoop, but we were unable to test whether or not it would run properly, so the argument `-r hadoop` was removed.

We consulted the nltk documentation, found at `http://www.nltk.org/`
We consulted the python3 json documentation, found at `https://docs.python.org/3/library/json.html`
We consulted the mrjob documentation, found at `https://pythonhosted.org/mrjob/`