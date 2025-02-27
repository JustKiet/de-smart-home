from abc import ABC, abstractmethod

class BaseSpeakerIDModel(ABC):
    @abstractmethod
    def torch_extract_speaker_vector(self, audio_file):
        raise NotImplementedError
    
    @abstractmethod
    def onnx_extract_speaker_vector(self, audio_file):
        raise NotImplementedError
    
    @abstractmethod
    def load_speakers_vectors(self):
        raise NotImplementedError
    
    @abstractmethod
    def save_speakers_vectors(self):
        raise NotImplementedError
    
    @abstractmethod
    def identify_speaker(self, audio_file, mode):
        raise NotImplementedError