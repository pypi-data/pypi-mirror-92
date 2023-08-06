""" Tests for NER tool """


def test_ner_tool():
    """The part below is commented for the test to execute quickly. Uncomment the code below to train a new model altogether, which takes quite a lot of time. The results from a trained model are saved in ner_tags.txt, which are used for testing.
    """
    # new_ner_tool = NerTool.create_new_ner_tool(
    #     model_name='some_name',
    #     version=Version.from_string("0.0.1"),
    #     save_model=False)
    # ner_tags, pos_tags = new_ner_tool.predict(
    #     sentence)
    # assertions are done within the predict.py file in ner_utils. It'll throw errors if something goes wrongs, for debugging purposes.
