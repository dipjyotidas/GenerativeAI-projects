#!pip install kili datasets evaluate ipywidgets openai scikit-learn numpy rich

import getpass
import json
import os
from collections import defaultdict

import numpy as np
import openai
from rich.console import Console
from rich.table import Table