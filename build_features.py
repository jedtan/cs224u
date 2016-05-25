# Any of the files in glove.6B will work here:
glove50_src = os.path.join(glove_home, 'glove.6B.50d.txt')

# Creates a dict mapping strings (words) to GloVe vectors:
GLOVE50 = utils.glove2dict(glove50_src)

def glove50vec(w):    
    """Return `w`'s GloVe representation if available, else return 
    a random vector."""
    return GLOVE50.get(w, randvec(w, n=50))

def build_dataset(
        wordentail_data, 
        vector_func=randvec, 
        vector_combo_func=vec_concatenate): 
    """
    Parameters
    ----------    
    wordentail_data
        The pickled dataset at `wordentail_data_filename`.
    
    vector_func : (default: `randvec`)
        Any function mapping words in the vocab for `wordentail_data`
        to vector representations
        
    vector_combo_func : (default: `vec_concatenate`)
        Any function for combining two vectors into a new vector
        of fixed dimensionality.
        
    Returns
    -------
    dataset : defaultdict
        A map from split names ("train", "test", "disjoint_vocab_test")
        into data instances:
        
        {'train': [(vec, [cls]), (vec, [cls]), ...],
         'test':  [(vec, [cls]), (vec, [cls]), ...],
         'disjoint_vocab_test': [(vec, [cls]), (vec, [cls]), ...]}
    
    """
    # Load in the dataset:
    vocab, splits = wordentail_data
    # A mapping from words (as strings) to their vector
    # representations, as determined by vector_func:
    vectors = {w: vector_func(w) for w in vocab}
    # Dataset in the format required by the neural network:
    dataset = defaultdict(list)
    for split, data in splits.items():
        for clsname, word_pairs in data.items():
            for w1, w2 in word_pairs:
                # Use vector_combo_func to combine the word vectors for
                # w1 and w2, as given by the vectors dictionary above,
                # and pair it with the singleton array containing clsname:
                item = [vector_combo_func(vectors[w1], vectors[w2]), 
                        np.array([clsname])]
                dataset[split].append(item)
    return dataset