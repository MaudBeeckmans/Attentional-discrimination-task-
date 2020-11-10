# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 17:53:04 2020

@author: Maud
"""

from psychopy import visual, core, event

speedy = 0

win = visual.Window(size = [800, 600], units = "deg", monitor = "Laptop")
                 
points_per_euro = 1000
points_per_trial = 10


spatie = '\n\n(Druk op spatie om verder te gaan)'
InstructionsP0 = str('Instructies: Het doel van de taak zal zijn een target te detecteren in 1 van 2 gepresenteerde '
                     +'gratings. De taak wordt in meer detail uitgelegd op volgende pagina\'s.' + spatie)
InstructionsP1 = str('\nElke trial zal beginnen met een fixatiekruis. Hiernaast zullen 2  '
                     + 'gratings verschijnen. Probeer je aandacht naar deze 2 gratings te richten, maar kijk ' 
                     + 'vooral steeds naar het fixatiekruis. Probeer dus geen oogbewegingen te maken.'
                     + spatie)
InstructionsP2 = str('Tijdens elke trial zal een flash rond één van de gratings verschijnen. Deze is totaal ' 
                     'IRRELEVANT voor de taak, probeer deze dus zo goed mogelijk te negeren.' + spatie)
InstructionsP3 = str('Het doel is de detectie van een target in één van de 2 gratings. Er is telkens evenveel kans ' 
                     + 'dat de target in de ene als de andere grating verschijnt. Geef aan in welke grating de ' 
                     + 'target verscheen met de toetsen f en j: \n\'f\' = LINKS      \'j\' = RECHTS.'
                     + '\nDoe dit zo snel, maar vooral ook zo ACCURAAT mogelijk.' + spatie)
InstructionsP4 = str('Geef ALTIJD een antwoord, ook als je de target niet hebt gezien. Antwoorden is mogelijk '
                     + 'vanaf de target is verschenen. Wanneer \'Antwoord!\' op het scherm verschijnt is je '
                     + 'tijd om te antwoorden bijna om. Geef dan zo snel mogelijk een antwoord.')
InstructionsP5 = str('Je zal zowel REWARD als NON REWARD blokken maken. In de REWARD blokken kan je punten verdienen:'
                     + '{} punten per correct antwoord. Per {} punten win je 1 EUR.'.format(points_per_trial, points_per_euro)
                     + 'In de NON REWARD blokken kan je geen punten verdienen. Aan het begin van elk blok wordt '
                     + 'het type blok aangegeven.' + spatie)
InstructionsP6 = str('Korte samenvatting van de belangrijkste zaken: '
                     + '\n     - Kijk steeds naar het fixatiekruis'
                     + '\n     - Negeer de flash'
                     + '\n     - Target altijd 50% kans om L als R te verschijnen'
                     + '\n     - Antwoordopties: links = \'f\', rechts = \'j\''
                     + '\n     - Geef ELKE TRIAL een antwoord'
                     + '\n     - REWARD blok: correct = punten (geld) verdienen')
InstructionsP7 = str('Moest je nog vragen hebben, kom dan gerust eens kloppen bij de proefleider. Deze helpt '
                     +'je zeer graag verder. Als je geen vragen meer hebt, gelieve dan je hoofd op de '
                     + 'hoofdsteun te leggen en vergeet niet steeds naar het fixatiekruis te kijken. Succes.' 
                     + spatie)

instructions_text = visual.TextStim(win, height = 0.1, units = 'norm', wrapWidth = 1.9, pos = (0, 0.5), alignText = 'left')
instructions_image = visual.ImageStim(win, image = None, pos = (0, -0.5), units = 'norm', size = (1.9, 1))
def instructions(page = 1): 
    if page == 0: 
        instructions_text.text = InstructionsP0
        instructions_text.pos = (0, 0)
        instructions_image.image = None
    elif page == 1: 
        instructions_text.text = InstructionsP1
        instructions_text.pos = (0, 0.5)
        instructions_image.image = "Instructies_Exp1.png"
    elif page == 2: 
        instructions_text.text = InstructionsP2
        instructions_text.pos = (0, 0.5)
        instructions_image.image = "Instructies_Exp2.png"
    elif page == 3: 
        instructions_text.text = InstructionsP3
        instructions_text.pos = (0, 0.5)
        instructions_image.image = "Instructies_Exp3.png"
    elif page == 4: 
        instructions_text.text = InstructionsP4
        instructions_text.pos = (0, 0)
        instructions_image.image = None
    elif page == 5: 
        instructions_text.text = InstructionsP5
        instructions_image.image = None
    elif page == 6: 
        instructions_text.text = InstructionsP6
        instructions_image.image = None
    elif page == 7: 
        instructions_text.text = InstructionsP7
        instructions_image.image = None
    instructions_text.draw()
    instructions_image.draw()
    win.flip()
    event.waitKeys(keyList = 'space')

for i in range(0, 8): 
    instructions(page = i)
win.close()









