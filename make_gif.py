import cv2
import os
import shutil
import subprocess

print('\n=================================\nConvert video to gif - v7\n=================================')
while True:
    print('\nPlease drag the video into this window or press Enter to exit:')
    vid = input('>>> ')
    if vid == '':
        break
    else:
        vid = vid.replace('"','')
        name = '.'.join(vid.split('/')[-1].split('.')[:-1])

        # Get video properties
        cap = cv2.VideoCapture(vid)
        video_fps = cap.get(cv2.CAP_PROP_FPS)

        ms_list = list(range(2,1001))
        fps_list = sorted(list(set([round(1/(x*0.01), 2) for x in ms_list])), reverse=True)

        print('--------------------------')
        # FPS and width
        print(f'\nVideo fps is {round(video_fps, 2)}fps')
        print('Please select gif fps: [10, 13, 17, 20, 25, 33, 50] or any number smaller than 10.\nIf leave blank, program will auto choose the closest one to video fps:')
        fps = input('>>> ')

        if fps == '':
            fps = min(fps_list, key=lambda x:abs(float(x)-video_fps))
        else:
            fps = min(fps_list, key=lambda x:abs(float(x)-float(fps)))
        print(f'GIF fps is {fps}')
        print('--------------------------')
        print(f'\nVideo width is {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}px')
        print('Please select gif width size (px). It cannot be larger than video width.\nIf leave blank, program will choose video width as final.')
        width = input('>>> ')

        if width == '':
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        else:
            width = int(width)

        print(f'GIF width is {width}px')

        print('--------------------------')
        # Extract video
        print('\nExtracting frames...\n')

        name_new = name
        count = 1
        while os.path.exists(f'{name_new}.gif'):
            name_new = f'{name}_{count}'
            count += 1
        name = name_new

        if os.path.exists('cv_temp'):
            shutil.rmtree('cv_temp')
        os.mkdir('cv_temp')
        i = 1
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            cv2.imwrite(f'cv_temp/{i:05d}.png', frame)
            i += 1
        cap.release()
        cv2.destroyAllWindows()

        # Convert to gif by gifski
        print('Converting to gif...\n')
        command = f"./gifski.exe -o '{name}.gif' --fps {fps} -W {width} --quality 100 cv_temp/*.png"
        subprocess.call(['powershell', command])
        shutil.rmtree('cv_temp')
        print('\n\n--------------------------\nFinish. Enjoy the gif\n--------------------------')
        # input('Enter to exit...')