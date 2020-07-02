from rank import rank

def main():
    results = {"worst": { "hello": {"tf": 4}, "tiger": {"tf": 8}, "apache": {"tf": 0}},
            "medium": { "hello": {"tf": 8}, "tiger": {"tf": 15}, "apache": {"tf": 4}},
            "best": { "hello": {"tf": 5}, "tiger": {"tf": 12}, "apache": {"tf": 15}}}

    query = {"hello": {"w": 0.5}, "tiger": {"w": 1.2}, "apache": {"w": 18}}

    test = rank(query, results, 3)

    #test if results are ordered correctly
    assert test[0][0] == "best"
    assert test[1][0] == "medium"
    assert test[2][0] == "worst"
    print("Ranker test ordered correctly.")

    test = rank(query, results, 1)

    assert len(test) == 1
    print("Ranker test returns correct number of docs.")

    print("Ranker tests passed.")

main()