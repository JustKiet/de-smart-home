from speaker_verification import VoiceIDService

def main():
    voice_service = VoiceIDService()

    new_user_id = voice_service.register_new_user("E:/Workspace/de-smart-home/backend/ai_modules/speech/new_user.wav")
    print(f"Người dùng mới được đăng ký với ID: {new_user_id}")

    # Kiểm tra nhận diện người nói
    test_file = "E:/Workspace/de-smart-home/backend/ai_modules/speech/test_voices/person_2_3.wav"
    result = voice_service.speaker_identifier.get_most_similar_speaker(test_file, "torch")
    
    print(f"Người nói được xác định là: {result}")

if __name__ == "__main__":
    main()
