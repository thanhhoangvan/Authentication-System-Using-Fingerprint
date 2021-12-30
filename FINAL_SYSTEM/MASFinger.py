import cv2 as cv
from glob import glob
import os
import numpy as np
from utils.poincare import calculate_singularities
from utils.segmentation import create_segmented_and_variance_images
from utils.normalization import normalize
from utils.gabor_filter import gabor_filter
from utils.frequency import ridge_freq
from utils import orientation
from utils.crossing_number import calculate_minutiaes
from utils.skeletonize import skeletonize

from MyMAS import MAS

# Config Cryptosystem
PIN = 123456
lenMask = 56

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
k = 3

def fingerprint_pipline(input_img):
    block_size = 16

    # normalization -> orientation -> frequency -> mask -> filtering

    # normalization - removes the effects of sensor noise and finger pressure differences.
    normalized_img = normalize(input_img.copy(), float(100), float(100))

    # color threshold
    # threshold_img = normalized_img
    # _, threshold_im = cv.threshold(normalized_img,127,255,cv.THRESH_OTSU)
    # cv.imshow('color_threshold', normalized_img); cv.waitKeyEx()

    # ROI and normalisation
    (segmented_img, normim, mask) = create_segmented_and_variance_images(normalized_img, block_size, 0.2)

    # orientations
    angles = orientation.calculate_angles(normalized_img, W=block_size, smoth=False)
    orientation_img = orientation.visualize_angles(segmented_img, mask, angles, W=block_size)
    
    # find the overall frequency of ridges in Wavelet Domain
    freq = ridge_freq(normim, mask, angles, block_size, kernel_size=5, minWaveLength=5, maxWaveLength=15)

    # create gabor filter and do the actual filtering
    gabor_img = gabor_filter(normim, angles, freq)

    # thinning oor skeletonize
    thin_image = skeletonize(gabor_img)

    # minutias
    minutias, end, bif = calculate_minutiaes(thin_image)

    # singularities
    singularities_img, FingerType = calculate_singularities(thin_image, angles, 1, block_size, mask)

    output_imgs = [input_img, minutias, singularities_img]

    return output_imgs, end, bif, FingerType

def DISTANCE(U, V) -> float:
    """
    """
    return np.sqrt((U[0] - V[0])**2 + (U[1] - V[1])**2)

def Points_distance(points1, points2) -> list:
    n = points1.shape[0]
    m = points2.shape[0]
    Distance = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            Distance[i, j] = DISTANCE(points1[i], points2[j])
    return Distance

def Filter_Points(ListPoints, CenterPoint, size = (0,0)):
    """
    """
    n = ListPoints.shape[0]
    ResultPoints = []
    for i in range(n):
        distance = np.abs(CenterPoint - ListPoints[i])
        if (distance[0] <= size[0]/2) and (distance[1] <= size[1]/2):
            ResultPoints.append(ListPoints[i].tolist())
    return np.array(ResultPoints)

def Transtation_Finger(Minutiae, Trans_Vector) -> np.ndarray:
    """
    """
    return Minutiae + Trans_Vector

def MATCH(finger1, finger2, alpha=0.5, box_size=(0, 0)) -> bool:
    """
    """
    # Get feature
    center_point1, end_1, bif_1 = finger1[0], finger1[1], finger1[2]
    center_point2, end_2, bif_2 = finger2[0], finger2[1], finger2[2]
    
    translation_vector = center_point2 - center_point1
    
    # Translation minutiaes
    end_1 = Transtation_Finger(end_1, translation_vector)
    bif_1 = Transtation_Finger(bif_1, translation_vector)
    
    # Filter minutiaes
    new_end_1 = Filter_Points(end_1, center_point2, size=box_size)
    new_bif_1 = Filter_Points(bif_1, center_point2, size=box_size)
    new_end_2 = Filter_Points(end_2, center_point2, size=box_size)
    new_bif_2 = Filter_Points(bif_2, center_point2, size=box_size)
    
    n1_end = new_end_1.shape[0]
    n1_bif = new_bif_1.shape[0]
    n2_end = new_end_2.shape[0]
    n2_bif = new_bif_2.shape[0]
    
    # Match ending points
    Distance_end = Points_distance(new_end_1, new_end_2)
    end_min_dist = Distance_end.min(axis=0)
    end_min_index = Distance_end.argmin(axis=0)
    
    # Match bifucation points
    Distance_bif = Points_distance(new_bif_1, new_bif_2)
    bif_min_dist = Distance_bif.min(axis=0)
    bif_min_index = Distance_bif.argmin(axis=0)
    
    # Check Matching
    end_matched = np.where(end_min_dist <= 15)[0].shape[0]
    bif_matched = np.where(bif_min_dist <= 15)[0].shape[0]
    
    if (end_matched + bif_matched)/(n1_end + n1_bif) >= alpha:
        return True
    else:
        return False
    
def FeaturesExtraction(finger):
    """
    """
    imgresult, end, bif, fingertype = fingerprint_pipline(finger)
    center_point = np.array(fingertype)[:,1:].astype(int).mean(axis=0)
    
    end = np.array(end)[:,1:]
    bif = np.array(bif)[:,1:]
    
    return [center_point, end, bif]

def S_Generation(PIN, lenMask) -> str:
    """
    """
    S = bin(PIN)[2:]
    n = len(S)
    k = lenMask//n
    
    return S*k + S[:lenMask - n*k]
        
def Features2Msg(features):
    """
    """
    center, end, bif = features[0].astype(int), features[1].astype(int), features[2].astype(int)
    
    center_msg = "{:3d}{:3d}".format(center[0], center[1]).replace(' ', '0')
    
    n = end.shape[0]
    m = bif.shape[0]
    
    end_msg = ''
    for point in end:
        end_msg += "{:3}{:3}".format(point[0], point[1]).replace(' ', '0')
    
    bif_msg = ''
    for point in bif:
        bif_msg += "{:3}{:3}".format(point[0], point[1]).replace(' ', '0')
    
    return "{}{:3}{:3}{}{}".format(center_msg, n, m, end_msg, bif_msg).replace(' ', '0')
    
def EncryptFinger(finger, PIN, A, B, X, Code, lenMask, k, padWord):
    """
    """
    # generation S
    # S = S_Generation(PIN, lenMask)
    S = b'10001101101011101000100011011010111010001110100011101000'
    print('generation Mask successful!')
    
    Msg = Features2Msg(finger)
    print('generation Msg successful!')
    
    cryptosystem = MAS(A, B, Code, X, S, k, padWord)
    
    EMsg = cryptosystem.Encode(Msg)
    
    with open("finger_saved.bin", "wb") as saved_finger:
        saved_finger.write(EMsg)

    return True

def Emsg2Features(EMsg, PIN, A, B, X, Code, lenMask, k, padWord):
    """
    """
    end = []
    bif = []
    
    S = b'10001101101011101000100011011010111010001110100011101000'
    print('generation Mask successful!')
    
    cryptosystem = MAS(A, B, Code, X, S, k, padWord)
    
    Result =  "".join(cryptosystem.Decode(EMsg))
    
    CenterPoint = np.array([Result[:3], Result[3:6]]).astype(int)
    n, m = int(Result[6:9]), int(Result[9: 12])
    
    t = 12
    for i in range(n):
        end.append([int(Result[t: t+3]), int(Result[t+3: t+6])])
        t += 6
    for i in range(m):
        bif.append([int(Result[t: t+3]), int(Result[t+3: t+6])])
        t += 6
    return [np.array(CenterPoint), np.array(end), np.array(bif)]

def SaveFinger(finger_path):
    image = cv.imread(finger_path, 0)
    finger_origin = FeaturesExtraction(image)
    if EncryptFinger(finger_origin, PIN, A, B, X, Code, lenMask, k, paddingWord):
        return True

def MatchFinger(finger_path):
    EMsg = b''
    with open("finger_saved.bin", "rb") as finger_saved:
        EMsg = finger_saved.read()
    finger_origin = Emsg2Features(EMsg, PIN, A, B, X, Code, lenMask, k, paddingWord)
    
    image = cv.imread(finger_path, 0)
    finger_match = FeaturesExtraction(image)   
    return MATCH(finger_origin, finger_match, box_size=(150, 300))

if __name__ == '__main__':
    
    # Save finger
    finger_path1 = './sample_inputs/101_1.tif'
    print(SaveFinger(finger_path1))

    # Reload saved finger and matching
    finger_path2 = './sample_inputs/101_2.tif'
    print(MatchFinger(finger_path2))