import array
import threading
from queue import Queue
import numpy as np

from modules.MLaughing.lpc import c_lpc, get_audio_frames
from modules.MLaughing.weight import WeightsAnimation

FPS = 30
SPEED_PLAY = float(1.0 / FPS)

bs_keys = ["brow_lower_l", "tongue_Scale__X", "tongue_Scale_Y", "tongue_Scale__Y", "tongue_Scale_Z", "tongue_Scale__Z", "nose_out_l", "nose_out_r", "tongue_u", "tongue_u_u", "brow_raise_d", "cheek_suck_r", "mouth_stretch_u", "tongue_u_d", "tooth_d_d", "tongue_d", "tooth_r", "tooth_d_u", "cheek_UP", "eye_blink1_l", "eye_blink1_r", "eye_blink2_l", "eye_blink2_r", "eye_lidTight_l", "eye_lidTight_r", "eye_shutTight_l", "eye_shutTight_r", "brow_lower_r", "eye_upperLidRaise_l", "eye_upperLidRaise_r", "eye_downLidRaise_l", "eye_downLidRaise_r", "jawLeft", "jawRight", "jawForward", "mouthClose", "mouthShrugLower", "mouthShrugUpper", "brow_raise_c", "mouthDimpleLeft", "mouthDimpleRight", "mouthFunnel", "mouth_funnel_dr", "mouth_funnel_ul", "mouth_funnel_ur", "mouth_lipCornerDepressFix_l", "mouth_lipCornerDepressFix_r", "mouthFrownLeft", "mouthFrownRight", "brow_raise_l", "mouth_lipCornerPullOpen_l", "mouth_lipCornerPullOpen_r", "mouthSmileLeft", "mouthSmileRight", "mouth_lipStretchOpen_l", "mouth_lipStretchOpen_r", "mouthStretchLeft", "mouthStretchRight", "mouthLowerDownLeft", "mouthLowerDownRight", "brow_raise_r", "mouth_lowerLipProtrude_c", "mouth_oh_c", "mouth_oo_c", "mouth_pressFix_c", "mouthPressLeft", "mouthPressRight", "mouthPucker", "mouth_pucker_r", "mouth_screamFix_c", "mouthLeft", "cheek_puff_l", "mouthRight", "jawOpen", "mouthRollLower", "mouth_suck_dr", "mouthRollUpper", "mouth_suck_ur", "mouthUpperUpLeft", "mouthUpperUpRight", "nose_wrinkle_l", "nose_wrinkle_r", "cheek_puff_r", "tooth_l", "eye_lookDown1_l", "eye_lookDown2_l", "eye_lookLeft_l", "eye_lookRight_l", "eye_lookUp_l", "eye_lookDown1_r", "eye_lookDown2_r", "eye_lookLeft_r", "eye_lookRight_r", "cheek_raise_l", "eye_lookUp_r", "tongue_Rot_1X", "tongue_Rot__1X", "tongue_Rot_2X", "tongue_Rot__2X", "tongue_Rot_3X", "tongue_Rot__3X", "tongue_Rot_1Y", "tongue_Rot__1Y", "tongue_Rot_2Y", "cheek_raise_r", "tongue_Rot__2Y", "tongue_Rot_3Y", "tongue_Rot__3Y", "tongue_Rot_1Z", "tongue_Rot__1Z", "tongue_Rot_2Z", "tongue_Rot__2Z", "tongue_Rot_3Z", "tongue_Rot__3Z", "tongue_Scale_X", "cheek_suck_l"]

const_bs_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 39, 46, 47, 48, 49, 50, 55, 56, 61, 62, 65, 70, 71, 72, 73, 83, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115]
# useful bs weight indices
var_bs_index = [10, 13, 14, 15, 18, 33, 38, 40, 41, 42, 43, 44, 45, 51, 52, 53, 54, 57, 58, 59, 60, 63, 64, 66, 67, 68, 69, 74, 75, 76, 77, 78, 79, 80, 81, 82, 84]
# default useless weight value
const_bs_value = [0.,0.,-0.,0.,-0.,0.,-0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,-0.,-0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,-0.,0.,-0.,0.,-0.,0.,-0.,0.,0.,-0.,0.,-0.,0.,-0.,0.,-0.,0.,-0.,0.]
# the sort of bs name correspond to UE input sort
bs_name_index = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 94, 93, 95, 96, 97, 98, 99, 100, 101, 102, 103, 105, 104, 106, 107, 108, 109, 110, 111, 112, 113, 114, 1, 115]

BS_CONUNT = 116

CPU_Thread = 1
CPU_Frames = 20

tflitepath = '/Users/tsurugiugushiro/Documents/HomeWork/2022.9/M-Intelligent_Prototype/modules/MLaughing/model/Audio2Face.tflite'
model_path = '/Users/tsurugiugushiro/Documents/HomeWork/2022.9/M-Intelligent_Prototype/modules/MLaughing/model/Audio2Face'
pb_weights_animation = WeightsAnimation(tflitepath, model_path)
get_weight = pb_weights_animation.get_weight

def worker(q_input, q_output, i):
    cnt = 0
    while True:
        input_data = q_input.get()
        for output_wav in input_data:
            output_lpc = c_lpc(output_wav)
            output_data = get_weight(output_lpc,label_len= len(var_bs_index))
            weights = np.zeros((output_data.shape[0],BS_CONUNT))
            weights[:,var_bs_index] = output_data
            weights[:,const_bs_index] = const_bs_value
            weights1 = np.zeros((output_data.shape[0],BS_CONUNT))
            for i in range(len(bs_name_index)):
                weights1[:,i] = weights[:,bs_name_index[i]]
            q_output.put(weights1)
        cnt += 1

class SoundAnimation:
    def __init__(self,cpus = 1,input_nums = 30):
        self.cpus = cpus
        self.input_nums = input_nums
        self.init_multiprocessing()
        self.flag_start = False

    def __del__(self):
        if self.flag_start:
            self.stop_multiprocessing()

    def init_multiprocessing(self):
        self.q_input = [Queue() for i in range(0, self.cpus)]
        self.q_output = [Queue() for i in range(0, self.cpus)]
        self.process = []
        for i in range(0, self.cpus):
            self.process.append(
                threading.Thread(target=worker, args=(self.q_input[i], self.q_output[i], i)))

    def start_multiprocessing(self):
        self.flag_start = True
        for i in range(0, self.cpus):
            self.process[i].setDaemon(True)
            self.process[i].start()
    
    def stop_multiprocessing(self):
        for i in range(0, self.cpus):
            self.process[i].terminate()
    
    def input_frames_data(self, input_date):
        input_data_nums = [input_date[i:i + self.input_nums] for i in range(0, len(input_date), self.input_nums)]
        self.flag_nums = len(input_data_nums)
        for i in range(0, self.cpus):
            self.q_input[i].put(input_data_nums[i::self.cpus])

    def yield_output_data(self):
        num = 0
        flag_end = True
        while flag_end:
            for i in range(0, self.cpus):
                if num == self.flag_nums:
                    flag_end = False
                    break
                data_output = self.q_output[i].get()
                for data in data_output:
                    yield data
                num += 1

sound_animation = SoundAnimation(CPU_Thread, CPU_Frames)
sound_animation.start_multiprocessing()

def a2fMain():

    with open("/Users/tsurugiugushiro/Documents/HomeWork/2022.9/M-Intelligent_Prototype/demo.wav", "rb") as f:
        b_wav_data = f.read()
    voice = np.frombuffer(b_wav_data[44:], dtype=np.int16)
    input_data = get_audio_frames(voice)
    try:
        sound_animation.input_frames_data(input_data)
        f_num = 0
        output = array.array('d')
        for weight in sound_animation.yield_output_data():
            f_num += 1
            for i in weight:
                output.append(i)
        #print(output)
        return output

    except Exception as err:
        print("Sound animation type error: ", err)

def emoChat():
    return a2fMain()
