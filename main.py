import os
import speech_recognition as sr  
import soundfile as sf
from pydub import AudioSegment
import pandas as pd
import json
import argparse




def load_wav_files_from_directory(root_directory):
    wav_files = []
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.wav'):
                wav_path = os.path.join(root, file)
                wav_files.append(wav_path)
            if file.endswith('.m4a'):
                wav_path = os.path.join(root, file)
                wav_files.append(wav_path)
            if file.endswith('.mp3'):
                wav_path = os.path.join(root, file)
                wav_files.append(wav_path)
    return wav_files

def convert_to_text(file):
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = r.listen(source)
        try:
            text = (r.recognize_google(audio,language='vi'))
        except:
            print("Sorry .. run again")
    return text

def get_duration_audio(file):
    if file.endswith('mp3'):
        mp3_file = AudioSegment.from_mp3(file)
        mp3_file.export(file.replace('mp3','wav'), format="wav")
        f = sf.SoundFile(file.replace('mp3','wav'))
        duration = f.frames / f.samplerate
    elif file.endswith('m4a'):
        mp3_file = AudioSegment.from_file(file)
        mp3_file.export(file.replace('m4a','wav'), format="wav")
        f = sf.SoundFile(file.replace('m4a','wav'))
        duration = f.frames / f.samplerate
    elif file.endswith('wav'):
        f = sf.SoundFile(file)
        duration = f.frames / f.samplerate
    return duration



def create_data_set_json(dir,out_save):
    list_path = load_wav_files_from_directory(dir)
    transcripts = []
    durations = []
    for file in list_path:
        text = convert_to_text(file)
        duration = get_duration_audio(file)
        transcripts.append(text)
        durations.append(duration)
    # save file json with pandas\
    data = [{'file': file, 'text': text, 'duration': duration} for file, text, duration in zip(list_path, transcripts, durations)]

    with open(out_save, 'w',encoding='utf-8') as json_file:
        for record in data:
            json.dump(record, json_file,ensure_ascii=False)
            json_file.write('\n')


def create_data_set_csv(dir,out_save):
    list_path = load_wav_files_from_directory(dir)
    transcripts = []
    durations = []
    for file in list_path:
        text = convert_to_text(file)
        duration = get_duration_audio(file)
        transcripts.append(text)
        durations.append(duration)
    # save file json with pandas\
    data = {'file': list_path, 'text': transcripts, 'duration': durations}
    df = pd.DataFrame(data)

    # Lưu DataFrame vào tệp CSV với định dạng UTF-8
    df.to_csv(out_save, index=False, encoding='utf-8')

def main(dir,type_save,out_save):
    if type_save == 'json':
        create_data_set_json(dir,out_save)
    if type_save == 'csv':
        create_data_set_csv(dir,out_save)


if __name__ =='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--dir',type=str,required=True,help="Choose a folder audio")
    parser.add_argument('--type',type=str,required=True,help="Choose a type json or csv")
    parser.add_argument('--output_save',type=str,required=True,help="path to save file dataset.json or dataset.csv")

    args = parser.parse_args()

    main(args.dir,args.type,args.output_save)