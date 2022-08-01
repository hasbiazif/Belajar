import speech_recognition as sr

engine = sr.Recognizer()
mic = sr.Microphone()
hasil = ""

with mic as source:
    print("Silahkan Mulai Berbicara")
    rekaman = engine.listen(source)
    print("Waktu habis")

    try:
        hasil = engine.recognize_google(rekaman, language = "id-ID")
        print(hasil)
    except engine.UnknownvalueError:
        print("Maaf tidak dideteksi, mohon coba lagi")
    except Exception as e:
        print(e)

#jika ingin simpan file
text_file = open("Hasil.txt", "w")
text_file.write(hasil)
text_file.close()