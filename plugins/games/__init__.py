from helpers.context import get_global_r, get_global_dev, get_global_k
r = get_global_r()
Dev_FINAL = get_global_dev()
k = get_global_k()
k = get_global_k()
Dev_FINAL = get_global_dev()
r = get_global_r()
from helpers.context import get_global_r, get_global_dev, get_global_k

try:
    from .bank import *
except ImportError as e:
    print(f"Failed to load bank_games: {e}")

try:
    from .marriage import *
except ImportError as e:
    print(f"Failed to load marriage: {e}")

try:
    from .words import *
except ImportError as e:
    print(f"Failed to load word_games: {e}")

try:
    from .questions import *
except ImportError as e:
    print(f"Failed to load quiz_games: {e}")

try:
    from .math import *
except ImportError as e:
    print(f"Failed to load math_games: {e}")

try:
    from .mediagames import *
except ImportError as e:
    print(f"Failed to load media_games: {e}")

try:
    from .addgame import *
except ImportError as e:
    print(f"Failed to load social_games: {e}")

try:
    from .quiz import *
except ImportError as e:
    print(f"Failed to load الكويز {e}")

try:
    from .farm import *
except ImportError as e:
    print(f"Failed to load المزرعه {e}")   

try:
    from .clubs import *
except ImportError as e:
    print(f"Failed to load الانديه {e}")         

try:
    from .devgames import *
except ImportError as e:
    print(f"Failed to load العاب المطور {e}")             
    
try:
    from .roulette import *
except ImportError as e:
    print(f"Failed to load الروليت {e}")             

try:
    from .utils import *
except ImportError as e:
    print(f"Failed to load ملف الدالة {e}")     
    
try:
    from .riddles import *
except ImportError as e:
    print(f"Failed to load ملف الغزاة {e}")                    
        
try:
    from .shop import *
except ImportError as e:
    print(f"Failed to load ملف متجري {e}")                    

try:
    from .hazr import *
except ImportError as e:
    print(f"Failed to load لعبة حزر {e}")
        
                