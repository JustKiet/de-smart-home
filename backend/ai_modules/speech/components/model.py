import time
import torch
import librosa
import pickle
import onnxruntime
from ruamel.yaml import YAML
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import importlib
import os
from ..interfaces.base_speakerid_model import BaseSpeakerIDModel



class NemoSpeakerIdentifier(BaseSpeakerIDModel):
    def __init__(self):
        self.threshold = 0.5
        self._init_onnx_model()
        # self._init_torch_model() 
        self.SIMILARITY_THRESHOLD = 0.4
        self.new_speaker_audio = None
        self.load_speakers_vectors()

    # def _init_torch_model(self):
    #     self.verification_model = nemo.collections.asr.models.EncDecSpeakerLabelModel.from_pretrained(model_name="speakerverification_speakernet")
    #     self.device = 'cpu'
    #     self.verification_model = self.verification_model.cpu()
    #     self.verification_model.eval()

    def _init_onnx_model(self):
        self.device = 'cpu'
        self.speakers_vectors_file = 'speakers_vectors_speakernet.pkl'
        speaker_model = 'speaker_model.onnx'
        self.sess = onnxruntime.InferenceSession(speaker_model)

        yaml = YAML(typ='safe')
        with open("model_config.yaml") as f:
            params = yaml.load(f)

        preprocessor_name = params['preprocessor']['_target_'].rsplit(".", 1)
        preprocessor_class = getattr(importlib.import_module(preprocessor_name[0]), preprocessor_name[1])
        preprocessor_config = params['preprocessor'].copy()
        preprocessor_config.pop('_target_')
        self.preprocessor = preprocessor_class(**preprocessor_config)

    def predict_speaker_vector(self, audio_file, mode):
        if mode == "torch":
            return self._torch_extract_speaker_vector(audio_file)
        if mode == "onnx":
            return self._onnx_extract_speaker_vector(audio_file)

# # def torch_predict_speaker_vector(self, audio_file) using to 
#     def _torch_extract_speaker_vector(self, audio_file):
#         audio, sr = librosa.load(audio_file, sr=16000)
#         audio_length = audio.shape[0]
#         audio_signal, audio_signal_len = (
#             torch.tensor([audio], device=self.device),
#             torch.tensor([audio_length], device=self.device),
#         )
#         _, embs = self.verification_model.forward(input_signal=audio_signal, input_signal_length=audio_signal_len)
#         emb_shape = embs.shape[-1]
#         embs = embs.view(-1, emb_shape)

#         return embs.cpu().detach().numpy()

    def _onnx_extract_speaker_vector(self, audio_file):
        audio, sr = librosa.load(audio_file, sr=16000)
        audio_length = audio.shape[0]
        audio_signal, audio_signal_len = (
            torch.tensor([audio], device=self.device),
            torch.tensor([audio_length], device=self.device),
        )

        processed_signal, processed_signal_len = self.preprocessor(
            input_signal=audio_signal, length=audio_signal_len,
        )

        _, embs = self.sess.run(None, {self.sess.get_inputs()[0].name: processed_signal.tolist(),
                                       self.sess.get_inputs()[1].name: processed_signal_len.tolist()})

        return embs

    def load_speakers_vectors(self):
        try:
            with open(self.speakers_vectors_file, 'rb') as f:
                self.speakers_vectors = pickle.load(f)
        except FileNotFoundError:
            self.speakers_vectors = {}

    def save_speakers_vectors(self):
        with open(self.speakers_vectors_file, 'wb') as f:
            pickle.dump(self.speakers_vectors, f)

    def add_speaker_vector(self, user_id, audio_file, mode):
        vector = self.predict_speaker_vector(audio_file, mode)
        self.speakers_vectors[user_id] = vector
        self.save_speakers_vectors()

    def get_most_similar_speaker(self, file, mode):
        self.consumed_time = []
        filepath = os.path.join("test_voices", file)

        if len(self.speakers_vectors) == 0:
            print("no speaker vector")

        start = time.time()
        vector = self.predict_speaker_vector(filepath, mode)

        speakers_vectors = [v[0] for v in self.speakers_vectors.values()]
        speakers_names = list(self.speakers_vectors.keys())

        sims = cosine_similarity([vector[0]], speakers_vectors)[0]
        end = time.time()
        print("Cosine similarity for {}: {}".format(file, sims))
        self.consumed_time.append(end-start)

        return self.consumed_time

    def identify_speaker(self, audio_file, mode="torch", threshold=None):
        if threshold is None:
            threshold = self.threshold

        if len(self.speakers_vectors) == 0:
            return "No registered speakers"

        # Trích xuất vector đặc trưng của âm thanh mới
        vector = self.predict_speaker_vector(audio_file, mode)

        # Lấy danh sách vector đã lưu
        speakers_vectors = [v[0] for v in self.speakers_vectors.values()]
        speakers_names = list(self.speakers_vectors.keys())

        # Tính độ tương đồng cosine
        sims = cosine_similarity([vector[0]], speakers_vectors)[0]

        # Lấy người có độ tương đồng cao nhất
        best_match_idx = np.argmax(sims)
        best_match_score = sims[best_match_idx]

        # In kết quả độ tương đồng
        print(f"Cosine similarities: {dict(zip(speakers_names, sims))}")

        # Nếu điểm số cao hơn threshold, xác nhận danh tính
        if best_match_score >= threshold:
            return speakers_names[best_match_idx]
        else:
            return "Unknown"