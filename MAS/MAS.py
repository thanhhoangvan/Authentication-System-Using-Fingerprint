import random
# random.seed(9)

class MAS:
    # Attributes
    __A = []
    __B = []
    __Code = {}
    __X = {}
    __S = 0b0 # Mask bit string
    __k = 0 # unambiguous degree of Language set
    __m = 0 # bit length of S
    __word_bit = 0 # bit length of code element
    __Padding_word = '' # word for pading
    
    # Constructor
    def __init__(self, A, B, Code, X, S, k, PaddingWord):
        self.__A = A
        self.__B = B
        self.__Code = Code
        self.__X = X
        self.__S = S
        self.__k = k 
        self.__m = len(self.__S) 
        self.__word_bit = len(list(self.__Code.values())[0])
        self.__Padding_word = self.__B.index(PaddingWord)
        print("MAS cryptosystem initialization successful!")
        print("Author: Thanh HoangVan")
        print("Github: thanhhoangvan")
        print("+-----------------------------------------+")
    
    # Methods
    def __Msg2Index(self, Msg, Dictionary) -> list:
        """
        Convert index of word to message by dictionary list
        ---
        Parameters:
        - Dictionary: List of all word
        - Msg: Message
        ---
        Return:
        - List of index word in message
        ---
        Example
        - Dictionary: ['c', 'a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'b4']
        - Message: "a1a2a3b1"
        - Return: [1, 2, 3, 4]
        """
        if len(Msg) == 0:
            raise Exception("Message is empty!")
        for i in Dictionary:
            Msg = Msg.replace(i, str(Dictionary.index(i)))
        return [int(i) for i in Msg]

    def __Index2Msg(self, WordIndex, Dictionary) -> str:
        """
        Convert index of word to message by dictionary list
        ---
        Parameters:
        - WordIndex: List of index word
        - Dictionary: List of all word
        ---
        Return:
        - Message string
        ---
        Example
        - Dictionary: ['c', 'a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'b4']
        - WordIndex: [1, 2, 3, 4]
        - Return: "a1a2a3b1"
        """
        Msg = ""
        for i in WordIndex:
            Msg = Msg + Dictionary[i]
        return Msg
    
    def __PlainText2Index(self, Msg='') -> list:
        """
        Split the words in the Message into a list of index this word in A
        ---
        Parameter:
        - Msg: a message(string)
        ---
        Retrun:
        - List of words
        ---
        Example:
        >>> A = ['u1', 'u2', 'u3']
        >>> __Msg2Index("u1u3u2u3") -> [0, 2, 1, 2]
        """
        if len(Msg) == 0:
            raise Exception("Message is empty!")
        for i in self.__A:
            Msg = Msg.replace(i, str(self.__A.index(i)))
        return [int(i) for i in Msg]

    def __EncodedMsg2Index(self, EMsg='') -> list:
        """
        """
        if len(msg) == 0:
            raise Exception("Encoded message is empty!")
        for i in self.__B:
            EMsg = EMsg.replace(i, str(self.__B.index(i)))
        return [int(i) for i in EMsg] # split index number to list    

    def __EncodedMsg2Binary(self, EMsg='') -> bytes:
        """
        Convert encoded message to binary result
        ---
        Parameter:
        - EMsg: String of encoded message(String)
        ---
        Result:
        - bytes string of result
        ---
        Example
        - Encoded message: 'ca1b1a2'
        with {'c': b'110', 'a1':b'001', 'a2':b'010', 'b1':b'100'}
        - Result: b'110001100010'
        """
        BinaryResult = b''
        if len(msg) == 0:
            raise Exception("Encoded message is empty!")
        word_index = self.__EncodedMsg2Index(EMsg)
        EMsg = [self.__B[i] for i in word_index] # split index number to list
        for i in EMsg:
            temp = self.__Code[i]
            BinaryResult = BinaryResult + temp
        return BinaryResult

    def __NormalizeLanguage(self) -> list:
        """
        Convet all word in X to list of index word
        ---
        Example
        ---
        -  X1 = {'c'}
        -  X2 = {'ca1', 'a1b1'}
        -  X3 = {'b1a2', 'ca1a3b1'}
        -  X4 = {'a2b2'}
        -  X5 = {'b2a3', 'a3'}
        -  X = [X1, X2, X3, X4, X5]
        => Result: X = [[[0]], [[0, 1], [1, 4]], [[0, 1, 3, 4], [4, 2]], [[2, 5]], [[3], [5, 3]]]
        """
        Normlized = []
        for i in self.__X:
            temp = []
            for word in i:
                temp.append(self.__Msg2Index(word, self.__B))
            Normlized.append(temp)
        return Normlized

    def __PADDING(self, EMsg) -> list:
        """
        Hàm đệm bit vào chuỗi
        """
        while len(EMsg)*self.__word_bit < self.__m:
            EMsg.append(self.__Padding_word)
        return EMsg
    
    def __EXTRACT(self) -> list:
        """
        Hàm phân tách tin nhắn thành list các từ
        """
        pass
    
    def __MASKING(self) -> bytes:
        """
        Hàm thêm lớp mặt nạ vào bit string đầu ra
        """
        pass
    
    def __e_g(self, k, Language) -> int:
        """
        Encode function
        ---
        Parameter:
        - k: index of Language
        - Language: List of Language
        ---
        Return
        ---
        - A random element corresponding to the index k
        """
        return random.choice(Language[k]) 
    
    def __d_g(self) -> list:
        """
        """
        pass
    
    def Encode(self, Msg="") -> bytes:
        """
        Encryption function
        ---
        
        Parameters
        ---
        - Msg: Messages to be encrypted
        
        Return
        ---
        - BitResult: The binary code of the encrypted message
        
        Example
        ---
        """
        
        # Check null message exception
        if len(Msg) == 0:
            raise Exception("Input message is empty!")
        
        Language = self.__NormalizeLanguage() # [[[0]], [[1, 4], [0, 1]], [[0, 1, 3, 4], [4, 2]], [[2, 5]], [[3], [5, 3]]]
        wordIndex = self.__PlainText2Index(Msg) # [0, 2, 4, 2, 3, 4, 1, 0, 2, 4]

        # initialization
        W = [] # list of all encode word in encoded msg
        i, j = 0, 0 # i_current msg word, j_current block bit of encode word(encoded msg)
        n = len(wordIndex) # number of word in message

        # main cryptosystem
        while True:
            count = 1
            temp = [] # Current encoded word
            while True:
                if (count >= self.__k) and (len(temp)*self.__word_bit >= self.__m): # Kiểm tra điều kiện độ dài từ W_j < m
                    if len(temp)*self.__word_bit < self.__m:
                        temp = self.__PADDING(temp)
                    
                    # Masking
                    # if j == 1:
                    #     pass
                    # else:
                    #     pass
                    
                    W.append(temp)
                    print('-'*20)
                    j = j + 1
                    break

              

                #============================================================
                newEncodedWord = self.__e_g(wordIndex[i], Language)
                
                if len(temp + newEncodedWord)*self.__word_bit <= self.__m:
                    temp = temp + newEncodedWord
                    count = count + 1
                    i = i + 1
                else:
                    temp = self.__PADDING(temp) 
                print(count, self.__k)
                print(temp, '\n')

            #============================================================
            if (i >= n):
                break # break first while loop
                
            
        return W
    
    def Decode(self) -> bytes:
        """
        """
        pass

if __name__ == '__main__':
    # Example Initialization
    A = ['u1', 'u2', 'u3', 'u4', 'u5']
    B = ['c', 'a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'b4']
    Code = {'c': b'110', 'a1':b'001', 'a2':b'010', 'a3':b'011', 'b1':b'100', 'b2':b'101', 'b3':b'000', 'b4':b'111'}
    # Language
    X1 = {'c'}
    X2 = {'ca1', 'a1b1'}
    X3 = {'b1a2', 'ca1a3b1'}
    X4 = {'a2b2'}
    X5 = {'b2a3', 'a3'}
    X = [X1, X2, X3, X4, X5]
    paddingWord = 'b4'
    k = 3
    # Message
    msg = 'u1u3u5u3u4u5u2u1u3u5'
    # Mask
    S = b'101000110110101100'

    #=======================================
    Cryptosystem = MAS(A, B, Code, X, S, k, paddingWord)
    print(Cryptosystem.Encode(msg))