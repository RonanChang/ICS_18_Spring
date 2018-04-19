'''
======================================================================
Name:Ruonan Chang
Github:
    https://github.com/RonanChang/ICS_18_Spring/tree/master/UP1-Ruonan-Chang
Aims:
    add_msg(1/1)
    indexing(1/1)
    deal_with_punctuations(1/1)
    search(1/1)
    search_for_phrases(1/1)
    deal_with_duplicates(1/1)
    load_poems(1/1)
    get_poems(1/1)
    deal_with_non-existing_poems_or_phrase(1/1)
    debugging(1/1)
    test_for_use(1/1)
======================================================================
'''
import pickle
from pprint import pprint

class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = [];
        self.index = {}
        self.total_msgs = 0
        self.total_words = 0
        
    def get_total_words(self):
        return self.total_words
        
    def get_msg_size(self):
        return self.total_msgss
        
    def get_msg(self, n):
        return self.msgs[n]
        
    # implement
    def add_msg(self, m):
        self.msgs.append(str(m)) #make sure m is a string
        self.total_msgs += 1
        
    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.total_msgs - 1
        self.indexing(m, line_at)

    # implement
    def indexing(self, m, l):
        '''
        At first I wanted to remove the dumplicates of words here:
        word_list = list(set(m.split(" ")))  
        but I can't do this anymore,
        because then the index of the words won't be accurate,
        and then searching for terms using index won't work accurately either
        '''
        
        word_list = m.split()
     
        #print(word_list) #debugging

        #Used to remove the punctuations after words    
        punctuations = ',.?!:;"\''
        
        for index,word in enumerate(word_list):
            #Pass if the word is the roman number
            if len(word_list) == 1 and word[-1] == '.' and word[-2].isupper():
                pass
            else:
                word = word.strip(punctuations)
            
            if word not in self.index.keys():
                self.index[word] = [(l,index)]
                
                # Only increase the total_words when the word hasn't been pushed in to the dictionary
                self.total_words += 1 
            else:
                #push the index of the word into the dictionary
                #so that we can use it when we are searching the phrase later
                self.index[word].append((l,index))
        
    # implement: query interface                     
    def search(self, term):
        '''
        return a list of tupple. if index the first sonnet (p1.txt), then
        call this function with term 'thy' will return the following:
        [(7, " Feed'st thy light's flame with self-substantial fuel,"),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (12, ' Within thine own bud buriest thy content,')]
                  
        ''' 
        
        words = term.split()
        #print(words) #debugging
        length = len(words)#used to check how many words we have
        #print(length)#debugging
        msgs = []
        
        if length <= 1: 
            #print(self.index.keys()) #debugging
            if term in self.index.keys():  
                
                #i is a tuple ---> (line_at,word_index)
                for i in self.index[term]:
                    #remove the duplicates
                    if (i[0],self.msgs[i[0]]) not in msgs:
                    #append a new tuple --> (line_at,message)
                        msgs.append((i[0],self.msgs[i[0]]))
            else:
                pass

        else:
            #first, find the lines where the first word exists
            try:
                #print(self.index[words[0]]) #debugging
                for i in self.index[words[0]]:
                    isFound = True
                    #checking other words
                    for j in range(1,length):
                        #check whether the next word in the sentence is wanted
                        if (i[0],i[1]+j) not in self.index[words[j]]:
                            isFound = False
                            break 
                    if isFound:
                        if (i[0],self.msgs[i[0]]) not in msgs:
                            msgs.append((i[0],self.msgs[i[0]]))
                
            except KeyError:
                return "Term not found!"
                
        #import pprint to achieve the result shown in the PDF prompt
        if len(msgs) == 0:
            return "Term not found!"
        return msgs
                        
                

class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        self.load_poems()
        
        # implement: 1) open the file for read, then call
        # the base class's add_msg_and_index
    def load_poems(self):
        poem_file = open(self.name,'r')
        line = poem_file.readline()
        while line != '':
            self.add_msg_and_index(line.strip())
            line = poem_file.readline()
        
    
        # implement: p is an integer, get_poem(1) returns a list,
        # each item is one line of the 1st sonnet
    def get_poem(self, p):
        try:
            #print(self.index)  #bebugging
            start_search = self.int2roman[p] + '.'
            #print(start_search) #debugging
            start_line = self.search(start_search)[0][0]
              
            try:
                end_search = self.int2roman[p+1] + '.'
                end_line = self.search(end_search)[0][0]
                
            #for the last sonnet in the file
            except:
                end_line = self.total_msgs
    
            poem = []
            for i in range(start_line,end_line):
                poem.append(self.msgs[i])
            pprint(poem) #Use pprint to make it prettier
            return poem
             
        except:
            print("Poem not found!")
            return

if __name__ == "__main__":
    sonnets = PIndex("AllSonnets.txt")
    # the next lines are just for testing
    print("================check for getting poems================")
    sonnets.get_poem(3) 
    print("================getting the last poem================")
    sonnets.get_poem(154)    
    print("================getting non-existing poems================")
    sonnets.get_poem(3000)   
    print("================search a single word================")
    s_love = sonnets.search("love")  
    pprint(s_love)
    print("================search for a phrase================")
    s_where_all = sonnets.search("where all")
    pprint(s_where_all)
    print("================search for a phrase================")
    s_forty_winters = sonnets.search("forty winters")
    pprint(s_forty_winters)
    print("================search for non-existing word================")
    s_null = sonnets.search("null")
    print(s_null)
    print("================search for non-existing phrases================")
    s_idk = sonnets.search("I dont know")
    print(s_idk)

    
    
