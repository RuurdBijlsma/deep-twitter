from textgenrnn import textgenrnn

textgen = textgenrnn()
print('-Default textgenrnn-')
textgen.generate()

textgen.train_from_file('tweets.txt', num_epochs=1)   
print('tweets fed::')
textgen.generate()

