#! /usr/bin/env python
""" Show pictures of crossed valence (pos/neg) and motivation (app/with).
Take responses with two buttons, one for each hand.
Ss do 2 blocks of trials. In one, they approach things with a left-handed
button press. In the other block, approach things with a right-handed 
button press. Counterbalanced order.
"""

SVE_DIRECTORY = '/Users/sway/Documents/Dropbox/Eugene Lang/Research/Casasanto Lab/VisionEgg/'
SVE_DIRECTORY = '/Users/Daniel_Casasanto/Documents/Scripts/cognac/'

import sys       
import csv
sys.path.append(SVE_DIRECTORY)  # add the SimpleVisionEgg functions to path
from random import shuffle, randint
from pygame import K_SPACE
from VisionEgg.Text import Text
from VisionEgg.WrappedText import WrappedText
from VisionEgg.Textures import Texture, TextureStimulus
from StimController import Response, Event, Trial, StimController
from SimpleVisionEgg import *

trial_index = 0


SUBJECT = raw_input('Participant: ')
time_point  = int(raw_input('Time (1/2/3/4): ')) 

# initialize vision egg
vision_egg = SimpleVisionEgg()
screen = vision_egg.screen
screen.parameters.bgcolor = (0, 0, 0)
xlim, ylim = vision_egg.screen.size # size of the screen in pixels

# a few useful stim objects
std_params = {'anchor': 'center', # for text display objects
              'position': (xlim/2, ylim/2), 'on': False}
fixation    = Text(text="+", font_size = 55, **std_params)
mask        = Text(text="XXXXXXXXXXX", font_size = 55, **std_params)
blank       = Text(text="", **std_params)
rest_screen = Text(text="Press SPACE to continue.", **std_params)

###########################
# A couple useful classes #
###########################
class TextStim(Text):
    """Stimulus text object"""
    def __init__(self, stim_string):
        self.stim_string = stim_string 
        
        Text.__init__(self, text=stim_string, font_size=50,
             color=[200,200,200],
             **std_params)


class ExpTrial(Trial):
    """Here's a trial for this experiment. It accepts a
    prime TextStim, a target TextStim, and a targe_type string.
    """
    def __init__(self, prime, target, condition):
        global trial_index
        trial_index += 1

        events=[Event(blank, start = 0, duration = 1),
                Event(fixation, start = 1, duration = .5),
#                Event(prime, start = 1.5, duration = 1.028),
#                Event(mask, start = 2.528, duration = 1.3),
#                Event(target, start = 3.828, duration = 5,
                Event(prime, start = 1.5, duration = .028),
                Event(mask, start = 1.528, duration = .3),
                Event(target, start = 1.828, duration = 5,
                      log={'Prime'      : prime._text, # Text class has a _text attribute for original string supplied.
                          'Target'      : target._text,
                          'Subject'     : SUBJECT,
                          'Trial'       : trial_index,
                          'Time'        : 'T' + str(time_point), 
                          'Condition' : condition},
                      response = Response(label = 'press', limit = ('z', "/")),
                      on_keypress = True)]                    

        Trial.__init__(self,events)  
        
class TreatmentTrial(Trial):
    """Here's a treatment trial for this experiment. It accepts
    US and CS TextStims, a target TextStim, and a gender (for logging).
    """
    def __init__(self, US, CS, target, gender):
        events=[Event(blank, start = 0, duration = 1),
                Event(fixation, start = 1, duration = .5),
#                Event(US, start = 1.5, duration = 1.028),
#                Event(CS, start = 2.528, duration = 1.028),
#                Event(mask, start = 3.556, duration = .3),
#                Event(target, start = 3.856, duration = 5,
                Event(US, start = 1.5, duration = .028),
                Event(CS, start = 1.528, duration = .028),
                Event(mask, start = 1.556, duration = .3),
                Event(target, start = 1.856, duration = 5,
                      log={'US'          : US._text,
                          'CS'           : CS._text,
                          'Prime'        : None,
                          'Target'       : target._text,
                          'Subject'      : SUBJECT,
                          'Time'         : 'T' + str(time_point), 
                          'Presentation' : 'Sequential'},
                      response = Response(label = 'press', limit = ('z', "/")),
                      on_keypress = True)]                    

        Trial.__init__(self,events)

class TreatmentTrial2(Trial):
    """Here's a trial for this experiment. It accepts a
    prim TextStim, a target TextStim, and a targe_type string.
    """
    def __init__(self, USCS, target, gender):
        events=[Event(blank, start = 0, duration = 1),
                Event(fixation, start = 1, duration = .5),
#                Event(USCS, start = 1.5, duration = 1.028),
#                Event(mask, start = 2.528, duration = .3),
#                Event(target, start = 2.828, duration = 5,
                Event(USCS, start = 1.5, duration = .028),
                Event(mask, start = 1.528, duration = .3),
                Event(target, start = 1.828, duration = 5,
                      log={'US'          : USCS._text.partition(' ')[0],
                          'CS'           : USCS._text.partition(' ')[2],
                          'Prime'        : None,
                          'Target'       : target._text,
                          'Subject'      : SUBJECT,
                          'Time'         : 'T' + str(time_point), 
                          'Presentation' : 'Simultaneous'},
                      response = Response(label = 'press', limit = ('z', "/")),
                      on_keypress = True)]                    

        Trial.__init__(self,events)
class InstructTrial(Trial):
    """ make instructions stim and trial given a sentence.
    <InstructTrial instance>.stim has to be passed to vision_egg.set_stimuli.
    """
    stim = None # Holds the VisionEgg stimulus object

    def __init__(self, sentence):
        self.stim = WrappedText(text = sentence, font_size = 50,
                                position=(xlim/2, ylim/2), on = False)
        
        events = [Event(blank, start = 0, duration = .3), 
            Event(self.stim, start = .3, duration = 1000, 
                on_keypress = True,  # end the event with a keypress
                response = Response(label = 'instruct', limit = 'space'))]                
        Trial.__init__(self, events)
        
#####################
# Set up the trials #
#####################
# Turn the strings of stimuli into TextStim objects
fixation = Text(text = "+", font_size = 55, **std_params)
REAL_KEY    = '?'
FAKE_KEY    = "Z" 

if time_point == 1:        
    # For T1, we want to just load the stimuli and shuffle them before presentation.
    # stimuli.csv has 3 entries per row, the prime, target, and whether it's a fear
    # positive, neutral, or pseudo set.

    # First, load the practice round with stims from T1_practice.csv
    prac_neutral_prime  = []
    prac_neutral_target = []
    prac_pseudo_prime   = []
    prac_pseudo_target  = []
    x = open('stim/T1_practice.csv', "rU")
    reader = csv.DictReader(x)
    for row in reader:
        if row['Condition'] == 'prac.neutral':
            prac_neutral_prime.append(row['Prime'])    
            prac_neutral_target.append(row['Target'])
        elif row['Condition'] == 'prac.pseudo':
            prac_pseudo_prime.append(row['Prime'])
            prac_pseudo_target.append(row['Target'])
        else:     
            print 'Prime was ', row['Prime']      
            print 'Target was ', row['Target']
            print 'Type was ', row['Condition'] 
            print 'Error with above entry, did not match condition.'
            quit()   

    prac_neutral_prime_list  = [TextStim(i) for i in prac_neutral_prime]
    prac_neutral_target_list = [TextStim(i) for i in prac_neutral_target]      
    prac_pseudo_prime_list   = [TextStim(i) for i in prac_pseudo_prime]
    prac_pseudo_target_list  = [TextStim(i) for i in prac_pseudo_target]

    prac_neutral_stimuli = []
    for i in range(len(prac_neutral_prime_list)):
        prac_neutral_stimuli.append((prac_neutral_prime_list[i], prac_neutral_target_list[i], 'prac.neutral'))

    prac_pseudo_stimuli = []
    for i in range(len(prac_pseudo_target_list)):
        prac_pseudo_stimuli.append((prac_pseudo_prime_list[i], prac_pseudo_target_list[i], 'prac.pseudo'))    

    
    dog_prime       = []
    fear_target     = []
    positive_seen_target    = []
    positive_unseen_target  = []
    neutral_prime   = []
    neutral_target  = []
    pseudo_prime    = []
    pseudo_target   = []
    x = open('stim/stimuli.csv', "rU")
    reader = csv.DictReader(x)
    for row in reader:
        if row['Condition'] == 'fear':
            dog_prime.append(row['Prime'])    
            fear_target.append(row['Target'])
        elif row['Condition'] == 'positive.seen':
            dog_prime.append(row['Prime'])
            positive_seen_target.append(row['Target'])
        elif row['Condition'] == 'positive.unseen':
            dog_prime.append(row['Prime'])
            positive_unseen_target.append(row['Target'])
        elif row['Condition'] == 'neutral':
            neutral_prime.append(row['Prime'])    
            neutral_target.append(row['Target'])
        elif row['Condition'] == 'pseudo':
            pseudo_prime.append(row['Prime'])
            pseudo_target.append(row['Target'])
        else:     
            print 'Prime was ', row['Prime']      
            print 'Target was ', row['Target']
            print 'Type was ', row['Condition'] 
            print 'Error with above entry, did not match condition.'
            quit()   

    dog_prime_list      = [TextStim(i) for i in dog_prime]
    fear_target_list    = [TextStim(i) for i in fear_target]
    positive_seen_target_list   = [TextStim(i) for i in positive_seen_target]
    positive_unseen_target_list = [TextStim(i) for i in positive_unseen_target]
    neutral_prime_list  = [TextStim(i) for i in neutral_prime]
    neutral_target_list = [TextStim(i) for i in neutral_target]      
    pseudo_prime_list   = [TextStim(i) for i in pseudo_prime]
    pseudo_target_list  = [TextStim(i) for i in pseudo_target]
    
    # Shuffle the fear and pseudo primes/targets.
    # Not done with neutral because they are on variety of topics
    # and the prime/target pair are hand-picked.
    shuffle(dog_prime_list)
    shuffle(fear_target_list)    
    shuffle(positive_seen_target_list)
    shuffle(positive_unseen_target_list)
    shuffle(pseudo_target_list)
    shuffle(pseudo_prime_list)
    
    # flat_list is used to pre-load the stimuli with vision_egg.set_stimuli
    flat_list = prac_neutral_prime_list + prac_neutral_target_list \
                + prac_pseudo_prime_list + prac_pseudo_target_list \
                + dog_prime_list + fear_target_list \
                + positive_seen_target_list + positive_unseen_target_list \
                + neutral_prime_list + neutral_target_list \
                + pseudo_prime_list + pseudo_target_list
    
    # For fear and positive stims, we are splitting the shuffled list of primes
    # called dog_prime_list and assigning 1/2 of it to the fear condition.
    # The remaining half we split in two and assign to the positive.seen and
    # positive.unseen conditions.
    fear_stimuli = []
    for i in range(len(dog_prime_list)/2):
        fear_stimuli.append((dog_prime_list[i], fear_target_list[i], 'fear'))

    positive_seen_stimuli = []
    for i in range(len(dog_prime_list)/4):
        positive_seen_stimuli.append((dog_prime_list[i + len(dog_prime_list)/2], positive_seen_target_list[i], 'positive.seen'))

    positive_unseen_stimuli = []
    for i in range(len(dog_prime_list)/4):
        positive_unseen_stimuli.append((dog_prime_list[i + (len(dog_prime_list)/4 * 3)], positive_unseen_target_list[i], 'positive.unseen'))
    
    neutral_stimuli = []
    for i in range(len(neutral_prime_list)):
        neutral_stimuli.append((neutral_prime_list[i], neutral_target_list[i], 'neutral'))
    
    pseudo_stimuli = []
    for i in range(len(pseudo_target_list)):
        pseudo_stimuli.append((pseudo_prime_list[i], pseudo_target_list[i], 'pseudo'))    
    
    combo_stimuli = fear_stimuli + positive_seen_stimuli + positive_unseen_stimuli \
                    + neutral_stimuli + pseudo_stimuli   
    shuffle(combo_stimuli) # Shuffle the order of prime/target pair presentation for T1 and T2
    
    prac_stimuli = prac_pseudo_stimuli + prac_neutral_stimuli
    shuffle(prac_stimuli)
    
    instruct_text = ["Welcome to the experiment!\n\nToday you'll see a variety of words presented one at a time.\nSome of these words will be real, and some will be fake.\n\nYour job is to quickly and accurately hit a key to categorize\n each word as real or fake.\n",
                     "Put your left index finger on the %s key.\nPut your right index finger on the %s key." % (FAKE_KEY, REAL_KEY),
                     "If the word is a REAL word,\npress the %s button with your right index finger.\n\nIf the word is a FAKE word,\npress the %s button with your left index finger.\n\nIt's important that you are both fast and accurate." % (REAL_KEY, FAKE_KEY),
                     "Real word:  %s\n\nFake word: %s" % (REAL_KEY, FAKE_KEY),
                     "First, you will have a chance to practice a few.\n\nReady to start?"]
    instruct_text = [s + "\n\nPress SPACE to continue." for s in instruct_text]
    instructions = [InstructTrial(s) for s in instruct_text]

    prac_over_text = ["Practice is now over.\n\nRemember to be as quick as you can while still being accurate."]
    prac_over_text = [s + "\n\nPress SPACE to continue." for s in prac_over_text]
    prac_over = [InstructTrial(s) for s in prac_over_text]

    prac_trials = [ExpTrial(prac_stimuli[i][0], prac_stimuli[i][1], prac_stimuli[i][2]) for i in range(len(prac_stimuli))]
    trials = [ExpTrial(combo_stimuli[i][0], combo_stimuli[i][1], combo_stimuli[i][2]) for i in range(len(combo_stimuli))]
    all_trials = instructions + prac_trials + prac_over + trials
    
    exp_stimuli = [rest_screen, fixation, mask, blank] + \
        [s.stim for s in instructions] + [s.stim for s in prac_over] \
        + flat_list
    
elif time_point >= 2:        
# Build the treatment task. Alternate between serial presentation
# and side-by-side presentation.
    flat_list = [] # gather all stimuli to feed set_stimuli
    treatment_stimuli = []
    treatment_trials = []
    a = 1
    x = open("stim/treatment.csv", "rU")
    reader = csv.DictReader(x)
    for row in reader:     
        if a == 1:
            US      = TextStim(row['US']) 
            CS      = TextStim(row['CS'])
            name    = TextStim(row['Name'])
            gender  = row['Gender']
            flat_list += [US, CS, name]
            treatment_trials += [TreatmentTrial(US,CS,name,gender)]
        elif a == 0:
            USCS = TextStim(row['US'] + ' ' + row['CS'])
            name    = TextStim(row['Name'])
            gender  = row['Gender']
            flat_list += [USCS, name]
            treatment_trials += [TreatmentTrial2(USCS,name,gender)]
        else:
            quit('a modulo was not 0 or 1!')
        a ^= 1                              

    shuffle(treatment_trials)
    
# For T2, read from the original file and keep all prime/target pairings.
# Combo_stimuli is shuffled for both T1 and T2 
    combo_stimuli = []         
    x = open("results/T1_%s_1.csv" %(SUBJECT), "rU")
    reader = csv.DictReader(x)
    for row in reader:
        if (row['Prime']) \
        and (row['Condition'] != 'prac.neutral') \
        and (row['Condition'] != 'prac.pseudo'):
            prime     = TextStim(row['Prime'])
            target    = TextStim(row['Target'])
            condition  = row['Condition']
            flat_list += [prime, target] # for set_stimuli
            combo_stimuli.append((prime, target, condition))

    shuffle(combo_stimuli) # Shuffle the order of prime/target pair presentation for T1 and T2        
    trials = [ExpTrial(combo_stimuli[i][0], combo_stimuli[i][1], combo_stimuli[i][2]) for i in range(len(combo_stimuli))]
                
    instruct_text = ["Welcome to the next section of the experiment.\n\nToday you'll see a variety of names presented one at a time.\nSome of these will be a boy's name, and some will be a girl's name.\n\nYour job is to quickly and accurately hit a key to categorize\n each name as a boy's name or girl's name.\n",
                     "Put your left index finger on the %s key.\nPut your right index finger on the %s key." % (FAKE_KEY, REAL_KEY),
                     "If the name is a BOY's name,\npress the %s button with your right index finger.\n\nIf the word is a GIRL's name,\npress the %s button with your left index finger.\n\nIt's important that you are both fast and accurate." % (REAL_KEY, FAKE_KEY),
                     "Boy's name:  %s\n\nGirl's name: %s" % (REAL_KEY, FAKE_KEY),
                     "Ready to start?"]
    instruct_text = [s + "\n\nPress SPACE to continue." for s in instruct_text]
    instructions = [InstructTrial(s) for s in instruct_text]


    instruct_text2 = ["Task complete.\n\nNext, you'll see a variety of words presented one at a time.\nSome of these words will be real, and some will be fake.\n\nYour job is to quickly and accurately hit a key to categorize\n each word as real or fake.\n",
                     "Put your left index finger on the %s key.\nPut your right index finger on the %s key." % (FAKE_KEY, REAL_KEY),
                     "If the word is a REAL word,\npress the %s button with your right index finger.\n\nIf the word is a FAKE word,\npress the %s button with your left index finger.\n\nIt's important that you are both fast and accurate." % (REAL_KEY, FAKE_KEY),
                     "Real word:  %s\n\nFake word: %s" % (REAL_KEY, FAKE_KEY),
                     "Ready to start?"]
    instruct_text2 = [s + "\n\nPress SPACE to continue." for s in instruct_text2]
    instructions2 = [InstructTrial(s) for s in instruct_text2]              
        
    all_trials = instructions + treatment_trials + instructions2 + trials        
                              
    exp_stimuli = [rest_screen, fixation, mask, blank] + \
        [s.stim for s in instructions] + [s.stim for s in instructions2] + flat_list
                
else:
    quit('Time must be 1, 2, 3, 4')    

###############
# Run the exp #
###############
vision_egg.set_stimuli(exp_stimuli)
stim_control = StimController(all_trials, vision_egg)

stim_control.run_trials(len(all_trials))
if time_point == 1:
    stim_control.writelog(stim_control.getOutputFilename('results/T1_' + str(SUBJECT), 'DP_LDT'))
else:
    stim_control.writelog(stim_control.getOutputFilename('results/T' + str(time_point) + '_' + str(SUBJECT), 'DP_LDT'))
    
print '\n\n\n\n\n\t\tThis section is complete. Please inform the experimenter.\n\n\n\n\n'
