import os
import tensorflow as tf
import numpy as np

class WeightsAnimation:

    def __init__(self, model_path, pb_model_path=None):
        self.model_path = model_path
        if not os.path.exists(model_path):
            self.convert_to_tflite(pb_model_path)
        # Load the model
        self.interpreter = tf.lite.Interpreter(model_path=model_path, num_threads=8)
        # Set model input
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()


    def convert_to_tflite(self, pb_model_path):
        # Convert the model from saved model(.pb) to tflite
        converter = tf.lite.TFLiteConverter.from_saved_model(pb_model_path)
        tflite_model = converter.convert()
        with open(self.model_path, "wb") as f:
            f.write(tflite_model)
        print(f'Save TFLite model to {self.model_path} successfully!')


    def run(self, inputData):
        # Preprocess the image before sending to the network.
        inputData = np.expand_dims(inputData, axis=0)
        # The actual detection.
        self.interpreter.set_tensor(self.input_details[0]["index"], inputData)
        self.interpreter.invoke()
        # Save the results.
        mesh = self.interpreter.get_tensor(self.output_details[0]["index"])[0]
        return mesh
    
    
    def get_weight(self, data, label_len=37):
        frame_num = data.shape[0]
        weight = np.zeros((frame_num, label_len), dtype=np.float32)
        for i in range(frame_num): 
            # print(f"frame is {i}")
            data_temp = data[i].astype(np.float32)
            # import pdb; pdb.set_trace()
            output = self.run(data_temp).reshape((1,-1))
            weight[i] = output
        return weight
