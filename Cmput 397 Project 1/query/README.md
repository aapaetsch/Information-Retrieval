[Assignment specs](https://sites.ualberta.ca/~denilson/cmput397-winter-2019-assignment-1.html)

# Don't forget to:

1. Make sure your program accepts the command line arguments in the order specified
1. Use the index you created by hand with a small corpus for developing and testing the query processing code in parallel
1. Document your design choices in the main `README.md` file

Assumptions: we must support boolean queries in our index, but we did not implement any way to input them in our queries. If the user has a boolean query file, our index can support it, but we ourselves have not implemented anything. Also, the input in the command line will always be accurate, ie we do not have to worry if the user inputs something other than `y` or `n`.

1. To run `vs_query.py`, use `python3 <path to vs_query.py> <path to index location> <number of docs to be retrieved> <y/n for scores> <query terms>` Note that all paths must end in `/` or you will receive an error message.

We made the decision to weight query with only idf because we wanted rare query terms to matter more than less ones, and to weight document terms with normalized tf scores only in order to focus on the relavancy of the document.