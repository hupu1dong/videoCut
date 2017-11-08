
from pydub import AudioSegment
from pydub.silence import split_on_silence
import random
import sys,os,math,re,argparse
#translate second into hour,minute,second
def sec2hms(msec):
	sec=mine=hour=0
	sec=round(msec)
	if((sec/60)>=1):
		mine=math.floor(sec/60)
		sec=sec%60
	if((mine/60)>=1):
		hour=mine/60
		mine=mine%60
	return int(hour),int(mine),int(sec)
def videocut(video_name):
	#initial all vaiable
	videonum=0
	start,dur,end=[],[],[0]
	#detect silence in video and write into txt
	#cmd='ffmpeg -i "cut0.mp4" -af silencedetect=noise=-45dB:d=0.35 -f null - 2> vol.txt'
	cmd='ffmpeg -i '+video_name+' -af silencedetect=noise=-45dB:d=0.35 -f null - 2> vol.txt'
	os.system(cmd)
	f=open('vol.txt','r')
	content=f.read()
	#saperate all start,end,during time of slience from txt
	pattern='silence_duration: [0-9]+.[0-9]+'
	pattern2='silence_start: [0-9]+.[0-9]+'
	pattern3='silence_end: [0-9]+.[0-9]+'
	start_slience=re.findall(pattern2,content,0)
	#put time into list
	for item in start_slience:
		start.append(item.split(': ')[1])

	end_slience=re.findall(pattern3,content,0)
	for item in end_slience:
		end.append(item.split(': ')[1])

	num=len(start)
	for item in range(num):
		dur.append(float(start[item])- float(end[item]))

	counter=0
	#if the video longer than 1s save it
	for pharse in range(num):
		startof_talk=end[pharse]
		durof_silence=dur[pharse]
		start_h,start_min,start_sec=sec2hms(float(startof_talk))
		dur_h,dur_min,dur_sec=sec2hms(durof_silence)
		'''
		#print the time interval
		print start_h,':',start_min,':',start_sec
		print dur_h,':',dur_min,':',dur_sec
		'''
		if dur_sec<=0:
			continue
		else:
			#save video
			cmd='ffmpeg -ss '+str(start_h)+":"+str(start_min)+":"+str(start_sec)+" -i "+video_name+\
			' -vcodec copy -acodec copy'+' -t '+str(dur_h)+":"+str(dur_min)+":"+str(dur_sec)+' ./resource/video_cut/'+str(videonum)+".mp4"
			os.system(cmd)
			#save as mp3
			del cmd
			cmd='ffmpeg -i'+' ./resource/video_cut/'+str(videonum)+".mp4 -f mp3 -ab 192000 -vn"+" ./resource/audio_mp3/"+str(videonum)+".mp3"
			os.system(cmd)
			videonum=videonum+1
			counter=counter+1

	print(num)
	print(counter)

if __name__ == "__main__":
	#for input argument

	parser = argparse.ArgumentParser(description='the mp4 file you want to spilt')
	parser.add_argument("file_name")
	args = parser.parse_args()
	videocut(args.file_name)


	#keyframe
	'''
	cmd='ffmpeg -i '+args.file_name+' -strict -2  -qscale 0 -intra '+args.file_name
	os.system(cmd)
 	 '''
