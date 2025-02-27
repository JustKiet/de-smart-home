import os
import time
from model import NemoSpeakerIdentifier

class VoiceIDService:
    
    def __init__(self):
        self.speakers_vectors = {}
        self.speaker_identifier = NemoSpeakerIdentifier()
        self.speaker_verification()
    
    def register_new_user(self, voice_path):
        if not self.speakers_vectors:
            new_user_id = "USER_1"
        else:
            # Lấy danh sách ID hiện tại và tìm ID mới
            existing_ids = set(self.speakers_vectors.keys())
            i = 1
            while f"USER_{i}" in existing_ids:
                i += 1
            new_user_id = f"USER_{i}"
        
        print(f"Registering new user: {new_user_id}...")
        
        # Thêm vector đặc trưng vào danh sách
        self.add_speaker_vector(new_user_id, voice_path, "onnx")

        print(f"New user {new_user_id} registered successfully!")
        print("Speakers in system:", list(self.speakers_vectors.keys()))
        
        return new_user_id
