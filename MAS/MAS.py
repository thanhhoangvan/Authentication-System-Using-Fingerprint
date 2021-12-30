import random
from itertools import chain
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
        self.__Padding_word = PaddingWord
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

    def __EncodedMsg2Binary(self, EMsg='') -> bytes:
        """
        Convert encoded message to binary result
        ---
        """
        BinaryResult = b''
        for eword in EMsg:
            for char in eword:
                BinaryResult += self.__Code[char]
            
        return BinaryResult

    def __Binary2Msg(self, bin_msg):
        """
        """
        chunks = [bin_msg[i:i+self.__word_bit] for i in range(0, len(bin_msg), self.__word_bit)]
        key_list = list(self.__Code.keys())
        val_list = list(self.__Code.values())
        
        Msg = ''
        for i in chunks:
            Msg += key_list[val_list.index(i)]
        
        word_size = self.__m // self.__word_bit
        
        Result = [Msg[i: i+word_size] for i in range(0, len(Msg), word_size)]
                
        return Result
        
    def __NormalizeLanguage(self) -> list:
        """
        Convet all word in X to list of index word
        ---
        """
        Normlized = []
        for i in self.__X:
            Normlized.append(i)            
        return Normlized

    def __PADDING(self, EMsg) -> list:
        """
        Hàm đệm bit vào chuỗi
        """
        while len("".join(EMsg))*self.__word_bit < self.__m:
            EMsg += self.__Padding_word
        return EMsg
    
    def __UNPADDING(self, EMsg) -> list:
        """
        """
        while self.__Padding_word in EMsg:
            EMsg = EMsg.replace(self.__Padding_word, '')
        return EMsg

    def __EXTRACT(self, Encoded_Word) -> list:
        """
        The function parses a list of letters and splits them into words
        ---
        """
        Language = list(chain.from_iterable(self.__NormalizeLanguage())) # List of all word in language [[0], [0, 1], [1, 4], [0, 1, 3, 4], [4, 2], [2, 5], [5, 3], [3]] 

        TMP = []
        W = ""

        def FIND(msg):
            m = len(msg)
            nonlocal W
            for j in msg:
                W += j
                if W in Language:
                    TMP.append(W)
                    W = ""
        
        for i in Encoded_Word:
            Unpad_Msg = self.__UNPADDING(i)
            n = len(Unpad_Msg)
            W = ""
            FIND(i)

        return TMP
        
    def __MASKING(self, EMsg=b'') -> bytes:
        """
        Hàm thêm lớp mặt nạ vào bit string đầu ra
        """
        # Generate mask
        n = len(EMsg)
        m = len(self.__S)
        k = n//m
        Mask = self.__S*k + self.__S[:(n-m*k)]

        Result = b''
        for i in range(len(EMsg)):
            if EMsg[i] == Mask[i]:
                Result += b'0'
            else:
                Result += b'1'
        return Result

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
        """
        char_index = self.__Msg2Index(Msg, self.__A)
        n = len(char_index) # length of msg
        W = []
        TMP = []
        i = 0
        
        while True:
            if i == n:
                break
            count = 0
            
            while True:
                try:
                    e_char = self.__e_g(char_index[i], self.__X)
                except:
                    if len(TMP)*self.__word_bit < self.__m:
                        TMP = self.__PADDING(TMP)
                    W.append("".join(TMP))
                    TMP = []
                    break

                if (len(TMP) + len(e_char))*self.__word_bit <= self.__m:
                    TMP.append(e_char)
                    count += 1
                    i += 1
                else:
                    TMP = self.__PADDING(TMP)

                if count == self.__k or len(TMP)*self.__word_bit  ==  self.__m:
                    if len(TMP)*self.__word_bit < self.__m:
                        TMP = self.__PADDING(TMP)
                    W.append("".join(TMP))
                    TMP = []
                    break

        return self.__MASKING(self.__EncodedMsg2Binary(W))
    
    def Decode(self, EMsg=[]) -> str:
        """
        Decryption function
        ---
        Parameters
        ---
        Return
        ---
        Example
        ---
        """
        # Check null message exception
        if len(EMsg) == 0:
            raise Exception("Input message is empty!")
        
        binary_msg = self.__MASKING(EMsg)
        EMsg = self.__Binary2Msg(binary_msg)

        Msg = []
        i, j = 0, 0
        n_word = len(EMsg)  # number of word in encoded message

        while True:
            
            Msg = []
            tmp = self.__EXTRACT(EMsg)
            for i in range(len(tmp)):
                for j in range(len(self.__X)):
                    if tmp[i] in self.__X[j]:
                        Msg.append(self.__A[j])

            return Msg
    