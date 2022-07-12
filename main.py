import os

#os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

import pytube
#import subprocess
from moviepy.audio.io.AudioFileClip import AudioFileClip

def convert_mp4_to_mp3(mp4, mp3):
    mp4_without_frames = AudioFileClip(mp4)
    mp4_without_frames.write_audiofile(mp3.replace(".mp4", "")) 
    mp4_without_frames.close()
    os.remove(mp4)

#def convert_mp4_to_mp3(download_path, mp4, mp3):
#    ffmpeg = (f'ffmpeg -i {download_path+mp4} {download_path+mp3}')
#    subprocess.run(ffmpeg, shell=True)
#    os.remove(mp4)

def busqueda():
    search = pytube.Search(input("Ingrese el video a buscar: "))
    list_of_results = search.results
    for i in range(len(list_of_results)-1):
        print(f"{i}. {list_of_results[i].title} from {list_of_results[i].author}")
    opcion = int(input("Ingresar numero de video o -1 para volver a buscar: "))
    if opcion == '-1':
        return busqueda()
    return list_of_results[opcion]

def playlist_downloader(main_op, download_path):
    while(True):
        url = input("Ingresar url de la playlist: ")
        sub = input(f"Ingresar subcarpeta o dejar en blanco para usar {download_path}: ")
        p = pytube.Playlist(url)
        i = 1
        for v in p.videos:
            if main_op == 1:
                name = v.streams.get_audio_only().default_filename
                namemp3 = name.replace(".mp4", ".mp3")
                if not os.path.isfile(download_path+"/"+sub+"/"+namemp3):
                    print(f'({i}/{p.length}) - Downloading from: {p.title} - {v.title}')
                    v.streams.get_audio_only().download(output_path=download_path+"/"+sub)
                    print(f"({i}/{p.length}) - Done.")
                    convert_mp4_to_mp3(download_path+"/"+sub+"/"+name, download_path+"/"+sub+"/"+namemp3)
                else:
                    print(f"({i}/{p.length}) - Ya tienes esta canción.")
            else:
                namemp4 = v.streams.get_highest_resolution().default_filename
                if not os.path.isfile(download_path+"/"+sub+"/"+namemp4):
                    print(f'({i}/{p.length}) - Downloading from: {p.title} - {v.title}')
                    v.streams.get_highest_resolution().download(output_path=download_path+"/"+sub)
                    print(f"({i}/{p.length}) - Done.")
                else:
                    print("El video actual ya está descargado.")
       	    i = i + 1
        
        print("""
                1. Ir al menu principal.
                2. Descargar otra playlist.
                """)         
        opcion = int(input("Ingresar una opción (1,2): "))
        if opcion == 1:
            break


def video_downloader(main_op, download_path):
    sub = input(f"Ingresar subcarpeta o dejar en blanco para usar {download_path}: ")
    while True:
        if main_op == 3:
            url = input("Ingresar url del video: ")
            video = pytube.YouTube(url)
        else:
            video = busqueda()
        print(f"Downloading {video.title} from Youtube")
        video.streams.get_highest_resolution().download(output_path=download_path+"/"+sub)
        print("Done.")
        print("""
                1. Ir al menu principal.
                2. Continuar descargando videos.
                3. Cambiar subcarpeta.
                """) 
        
        opcion = int(input("Ingresar una opción (1,2,3): "))

        if opcion == 1:
            break
        elif opcion == 3:
            sub = input(f"Ingresar subcarpeta o dejar en blanco para usar {download_path}: ")

def song_downloader(main_op, download_path):
    sub = input(f"Ingresar subcarpeta o dejar en blanco para usar {download_path}: ")
    while True:  
        if(main_op == 5):
            url = input("Ingresar url del video: ")
            cancion = pytube.YouTube(url)
        else:
            cancion = busqueda()
        name = cancion.streams.get_audio_only().default_filename
        namemp3 = name.replace(".mp4", ".mp3")
        if not os.path.isfile(download_path+"/"+sub+"/"+namemp3):
            print(f"Downloading {cancion.title} from Youtube")
            cancion.streams.get_audio_only().download(output_path=download_path+"/"+sub)
            print("Done.")
            convert_mp4_to_mp3(download_path+"/"+sub+"/"+name, download_path+"/"+sub+"/"+namemp3)
            #convert_mp4_to_mp3(download_path+"/"+sub+"/", name, namemp3)
        else:
            print("Ya tienes esta canción.")
        

        print("""
                1. Ir al menu principal.
                2. Continuar descargando canciones.
                3. Cambiar subcarpeta.
                """) 
        
        opcion = int(input("Ingresar una opción (1,2,3): "))
        if opcion == 1:
            break
        elif opcion == 3:
            sub = input(f"Ingresar subcarpeta o dejar en blanco para usar {download_path}: ")


download_path = input(""" 
            Bienvenido a mi Youtube Downloader!  

        Ingresar path default para descargas: """)

while(True):

    print(""" 
            MAIN MENU:
        
        1. Descargar una playlist en solo sonido by url.
        2. Descargar una playlist video max quality by url.
        3. Descargar un video max quality by url.
        4. Descargar un video max quality by busqueda.
        5. Descargar una canción by url.
        6. Descargar una canción by busqueda.
        7. Finalizar el programa.
        
        """)
    opcion = int(input("Ingrese una opción (1,2,3,4,5,6,7): "))
    
    if opcion == 7:
        break
    elif opcion == 1 or opcion == 2:
        playlist_downloader(opcion, download_path)
    elif opcion == 3 or opcion == 4:
        video_downloader(opcion, download_path)
    else: 
        song_downloader(opcion, download_path)
        