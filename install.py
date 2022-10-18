import os
from pathlib import Path
if not os.path.exists(os.path.join(Path.home(),'DigitadorOrbi')):
    os.mkdir(f'{Path.home()}/DigitadorOrbi')
if not os.path.exists(os.path.join(f'{Path.home()}/DigitadorOrbi','xmlssw')):
    os.mkdir(f'{Path.home()}/DigitadorOrbi/xmlssw')
if not os.path.exists(os.path.join(f'{Path.home()}/DigitadorOrbi','XMLs')):
    os.mkdir(f'{Path.home()}/DigitadorOrbi/XMLs')