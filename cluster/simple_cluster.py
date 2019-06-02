def func():
    # put reader and map function are combined
    words = ['боль', 'страдания']
    word = words[random.randint(1)]
    print (word)
    return word

if __name__ == '__main__':
    import dispy, logging
    # assume nodes node1 and node2 have 'doc1', 'doc2' etc. on their
    # local storage, so no need to transfer them
    cluster = dispy.SharedJobCluster(computation=func, scheduler_node='192.168.43.74')
    job = cluster.submit()
    word = job()
    print(word)
    print('worked')