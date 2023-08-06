""" Tests for text_augmenter tool """


def test_augmented_text():
    """The part below is commented for the test to execute quickly. Uncomment the code below to train a new model altogether, which takes quite a lot of time. The results from a trained model are saved in augmented_text.txt, which are used for testing.
    """
    # new_augmenter_tool = TextAugmenterTool.create_new_augmenter(
    #     model_name='some_name',
    #     version=Version.from_string("0.0.1"),
    #     text_iter=corpus,
    #     save_model=False)
    # augmented_result = new_augmenter_tool.augment_batch(
    #     text_iter_n=5)
    # f = open('sermos_tools/catalog/text_augmenter/data/augmented_text.txt', 'w')
    # f.write(augmented_result)
    # f.close()

    f = open('sermos_tools/catalog/text_augmenter/data/augmented_text.txt',
             'r')
    augmented_result = f.read().split('\n')

    assert isinstance(augmented_result[0], str)