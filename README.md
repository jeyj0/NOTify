# FB-ML-Hackathon

Prepare data:

`$ python prepareData.py`

Train a new model:

`$ ./fastText/fastText supervised -input training_data.txt -output slack_model`

Test model:

`$ ./fastText/fastText test slack_model.bin validation_data.txt`
