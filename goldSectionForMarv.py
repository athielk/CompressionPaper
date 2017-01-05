import math
import pygame
import random
import time
import sys

golden = 2 / (1 + 5 ** .5)
LENGTHOFWAV=4



class golden_section_queue(object):
    def __init__(self,wavs,templete_wav):
        super(golden_section_queue,self).__init__()
        self.wavs=wavs
        self.templete_wav=templete_wav
        self.low=0
        self.high=len(wavs)

    def __len__(self):
        return len(self.wavs)

    def __str__(self):
        return "low %i and high %i"%(self.low,self.high)


    def _find_upper(self):
        index = int(math.ceil(self.low + golden * (self.high - self.low)))
        if index == self.high:
            index -= 1
        return index


    def _find_lower(self):
        index = int(math.floor(self.high - golden * (self.high - self.low)))
        if index == self.low:
            index += 1
        return index


    def update(self,result):
        '''
        :param result: 1 for left button pressed 2 for right button pressed
        :return:
        '''
        if result==1:#update lower
            index= self._find_lower()
            self.low=index
        elif result==2:#update high
            index= self._find_upper()
            self.high=index
        else:
            raise ValueError("result %i not expected only excepts 1,2"%(result))


    def next(self):
        '''
        :return: a trial
        '''
        low_tmp = self._find_lower()
        high_tmp = self._find_upper()
        return [self.templete_wav,self.wavs[low_tmp],self.wavs[high_tmp]]

class mixed_queue(object):
    def __init__(self,queues):
        super(mixed_queue,self).__init__()
        self.queues=queues
        self.next_queue=None

    def update(self,result):
        if self.next_queue==None:
            raise RuntimeError("update called before next.")
        self.queues[self.next_queue].update(result)
        self.next_queue=None

    def next(self):
        '''
        :return: a trial of random queue in collection
        '''
        self.next_queue=random.randint(0,len(self.queues)-1)
        return self.queues[self.next_queue].next()

    def __len__(self):
        return len(self.queues)

def run():
    pygame.init()
    pygame.display.set_mode((100, 100))
    # trial=['bird.wav', 'bird.wav', 'bird.wav']
    queue = golden_section_queue(['bird.wav', 'bird.wav', 'bird.wav'], 'bird.wav')
    mixed=mixed_queue([queue,queue])
    print queue
    #trial_queue = mixed_queue(queue)
    #trial = trial_queue.next()
    step(mixed)
    step(mixed)
    step(mixed)

def step(queue):
    trial = queue.next()
    result = run_trial(trial)
    print result
    queue.update(result)
    print queue

def play_wav(wav):
    pygame.mixer.init()
    song = pygame.mixer.Sound(wav)
    song.play()
    time.sleep(LENGTHOFWAV)

def run_trial(trial):
    for i in trial:
        play_wav(i)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return 1
                if event.key == pygame.K_RIGHT:
                    return 2
                if event.key == pygame.K_UP:
                    return run_trial(trial)

if __name__ == "__main__":
    run()