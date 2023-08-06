import os
import sys
import numpy as np
from tensorflow import keras
file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(file_path)
project_directory = os.path.dirname(current_directory)
sys.path.insert(0, project_directory)
from {{ package_name }}.models import {{ project_name }}

# load model in development mode
model_path = os.path.join(project_directory, 'saved_models', '{{ package_name }}')
model = {{ project_name }}().load_model(model_path)

sample_text = [
    'The movie was cool. The animation and the graphics were out of this world. I would recommend this movie.',
    
    "I saw this film as it was the second feature on a disc containing the previously banned Video Nasty 'Blood Rites'. \
    As Blood Rites was entirely awful, I really wasn't expecting much from this film; but actually, it would seem that trash \
    director Andy Milligan has outdone himself this time as Seeds of Sin tops Blood Rites in style and stands tall as a more than \
    adequate slice of sick sixties sexploitation. The plot is actually quite similar to Blood Rites, as we focus on a \
    dysfunctional family unit, and of course; there is an inheritance at stake. The film is shot in black and white, and \
    the look and feel of it reminded me a lot of the trash classic 'The Curious Dr Humpp'. There's barely any gore on display, \
    and the director seems keener to focus on sex, with themes of incest and hatred seeping through. The acting is typically \
    trashy, but most of the women get to appear nude at some point and despite a poor reputation, director Andy Milligan actually \
    seems to have an eye for this sort of thing, as many of the sequences in this film are actually quite beautiful. The plot is \
    paper thin, and most of the film is filler; but the music is catchy, and the director also does a surprisingly good job with \
    the sex scenes themselves, as most are somewhat erotic. Overall, this is not a great film; but it's likely to appeal to \
    the cult fan, and gets a much higher recommendation than the better known and lower quality 'Blood Rites'."
]

for x, y in zip(sample_text, model(sample_text)):
    print(f"\nreview: {x}\nscore: {y}\n")