import os, glob

path = '20_newsgroups'                              #path of the dataset
folders = os.listdir(path)                          #list of folders present in the dataset 

#Function to check the probability of a file for a praticular place.
#It takes list of words in a file, dictionary of that class to check and index 
#of that class in folders list and outputs sum of probabilities of all the words
def CheckProbability(testWords, bag, number):
    size = sizes[number]                            #Taking the size of the dictionary
    p = 0
    for t in testWords:
        weightage = bag_of_words[f].get(t, 0)       #count of the word in a class dictionary
        check = total_words.get(t, 0)               #count of the word in teh entire vocabulary
        probability = ((weightage+1)/(size+total))  #Probability calculation
        if check != 0:                              #If the word is present in vocabulary, add the probability
            p = p + probability
    return p 

#Function to do data cleaning.
#Removing all special symbols and stop words that are not useful in classification
def clean(fileData):
    fileData = fileData.replace('\n', ' ')          #Removing next line
    fileData = fileData.lower()                     #Lower case all the data
    fileData = fileData.translate({ord(z): None for z in '0123456789'})   #Removing digits from the data
    removeList = ['<','>','?','.','"',')','(','|','-','_','#','*','+','"','$']
    replaceList = ["'",'!','/','=',',',':','\\']
    stopWords = ['a', 'about', 'above', 'after', 'again', 'against', 'aint', 'all', 'am', 'an', 'and', 'any', 'are', 'arent',
                 'aren', 'isn', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 
                 'can', 'couldn', 'couldnt', 'could', 'd', 'did', 'didnt', 'didn', 'do', 'does', 'doesnt', 'doesn', 'doing', 
                 'dont', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadnt', 'has', 'hasnt', 'have', 'shan', 
                 'havent', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 
                 'into', 'is', 'isnt', 'it', 'its', 'don', 'itself', 'just', 'll', 'm', 'ma', 'me', 'mightnt', 'more', 'most', 
                 'mustnt', 'my', 'myself', 'neednt', 'needn' 'no', 'nor', 'not', 'now', 'o', 'of', 'off', 'on', 'once', 'only', 
                 'or', 'other', 'our', 'ours', 'b', 'r', 'w', 'ourselves', 'out', 'over', 'own', 're', 's', 'same', 'shant', 
                 'she', 'should', 'shouldnt', 'so', 'shan', 'hadn', 'hasn', 'haven', 'wouldn', 'also', 'mightn', 'ain', 'wasn',
                 'some', 'such', 't', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'weren', 
                 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 've', 'very', 'was', 
                 'wasnt', 'we', 'were', 'werent', 'what', 'when', 'where', 'which', 'while', 'who', 'x', 'c', 'whom', 'why', 
                 'will', 'with', 'won', 'wont', 'wouldnt', 'y', 'you', 'your', 'yours', 'yourself', 'yourselves', 'would', 'gmt',
                 'xref', 'us', 'one', 'two', 'like', 'know', 'lines', 'messageid', 'mustn', 'shouldn']
    for x in removeList:
        fileData = fileData.replace(x,'')
    for x in replaceList:
        fileData = fileData.replace(x,' ')
    fileData = [word for word in fileData.split() if word not in stopWords]
    return fileData  

#Dictionaries for training and testing sets
bag_of_words = {}
total_words = {}
testing_files = {}

print ("Building bag of words ...")

#Building class dictionary and total dictionary (vocabulary) for the first 500 files in each folder
#Taking the remaining files in every folder for testing
for f1 in folders:
    temp = {}
    files = glob.glob(os.path.join(path, f1, '*'))
    for f2 in files[:500]:
        with open(f2) as f:
            data = clean(f.read())
            #For each word in a file, check if it exits in the dictionary. If yes, increment the counter. Else add the word
            for w in data:
                count_in_bag = temp.get(w, 0)
                count_in_total = total_words.get(w, 0)
                if count_in_bag == 0:
                    temp[w] = 1
                else:
                    temp[w] = count_in_bag + 1
                if count_in_total == 0:
                    total_words[w] = 1
                else:
                    total_words[w] = count_in_total + 1
    bag_of_words[f1] = temp
    testing_files[f1] = files[500:]

total = len(total_words)                            #Length of the vocabulary    

print (total, 'is the Length of Training set')

sizes = []                                          #List to keep track of total words in each class's dictionary
for f in folders:
    sizes.append(sum(bag_of_words[f].values()))
    
print ("Testing ...")

success = 0                                         #To keep track of number of successes while testing files
count = 0                                           #To know the number of test files

#Testing the files
for folder in folders:
    for testFile in testing_files[folder]:
        count = count + 1
        with open(testFile) as file:
            data = clean(file.read())
        prob = []
        #Check the probability of each file for every class. Taking the maximum probability class as required answer. 
        for f in folders:
            prob.append(CheckProbability(data, bag_of_words[f], list(bag_of_words.keys()).index(f)))
        #If derived class macthes the file's original class, then increment success
        if folders[prob.index(max(prob))]  == folder:
            success = success + 1
                            
Accuracy = success / count                          #Calculating accuracy
print ("Accuracy of the classification is", Accuracy*100)