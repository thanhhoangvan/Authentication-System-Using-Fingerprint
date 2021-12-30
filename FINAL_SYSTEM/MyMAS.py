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
        
        

if __name__ == '__main__':
    # Example Initialization
    A = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    B = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n','o', 'p']
    Code = {'a': b'1000',
            'b': b'1110',
            'c': b'0011', 
            'd': b'1111', 
            'e': b'1101', 
            'f': b'0010', 
            'g': b'1100', 
            'h': b'0101',
            'i': b'1011',
            'j': b'0000',
            'k': b'1001',
            'l': b'0111',
            'm': b'0100',
            'n': b'1010',
            'o': b'0001',
            'p': b'0110'}
    
    # Language
    X0 = ['a', 'cgh']
    X1 = ['egm', 'nmc']
    X2 = ['ig', 'fce']
    X3 = ['jkd']
    X4 = ['bea', 'mok']
    X5 = ['fno', 'ihc']
    X6 = ['cei']
    X7 = ['demc', 'khm']
    X8 = ['lbkh']
    X9 = ['kog', 'dcef']
    X = [X0, X1, X2, X3, X4, X5, X6, X7, X8, X9]
    paddingWord = 'p'
    k = 4
    
    # Message
    msg ='184288166026015170015182015200015219015244015270015295015305015330015359015389016302018135018149018163018421018427019433022131024421025438026445027434032446034103034114034472036458038099038468039474040446041462043454044358046428050087050480052480054210054483055256057494058080059479061079061168061401062078062481063491064333066072075066078448079471080251080506095530096110096174096524098536099056100113101302108539114500115540116050119533123381130191132206132371132456133143137355139409139495141337144448145345146176151126156303157181158238160349161153161446163473164050171478173057185536187315189335190309190494191256191265192270195320195521196141198317200210202333202481208356211192214545217069219155220457221537224075225541228079231083233318234527235400235538237164240528241354241524245082246307248211251524252085252230254133255091256111259513262351263287264423267506269121269500273499279153280475280490281138281146281164281181281200281215281228281247281267281289281316281397281414281432281445281460281484016175032407043440065488081344089512095527096527100354157235159148159153160231184270190258192320193249194302194335201317206354223077226532252095256369277489'
    
    # Mask
    S = b'10001101101011101000100011011010111010001110100011101000'
    

    #=======================================
    Cryptosystem = MAS(A, B, Code, X, S, k, paddingWord)
    # Encode message
    EMSG = Cryptosystem.Encode(msg)
#     print(len(msg))

    MSG = Cryptosystem.Decode(EMSG)
    
    Result = "".join(MSG)
#     print(Result == msg)
#     print(len(msg), len(Result))
    print(Result)