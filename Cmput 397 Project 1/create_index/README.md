[Assignment specs](https://sites.ualberta.ca/~denilson/cmput397-winter-2019-assignment-1.html)

# Don't forget to:

1. Make sure your program accepts the command line arguments in the order specified
1. Create an index by hand with a small corpus which you can use for testing and for developing the query processing code in parallel
1. Make sure your non-Map/Reduce code is going to work **before** you start with Map/Reduce
1. Test your index creation carefully

Assumptions: we must support boolean queries in our index, but we did not implement any way to input them in our queries. If the user has a boolean query file, our index can support it, but we ourselves have not implemented anything. We assume that the assign says nothing about actually having to implement boolean queries, merely that our index must support them.

1. To install nltk, run `pip3 install nltk`
2. To run `create_index.py`, use `python3 <path to create_index.py> <path to index directory>`
3. In order to install mapreduce, `pip3 install mrjob`
4. To run the mapreduce `create_index.py`, use the same command but call the `create_index.py` that is in the map_reduce folder.

Our error handling strategy is to split on the extension (ex test.txt splits to test and txt) and then verify that the file is a txt file. If not, we raise an error and move on to the next file. This ensures that the files we intake are in a standard format that we know we can read and index. Emojis are ignored, unicode characters are indexed as their unicode name (ex ä is encoded as /u00e4)
