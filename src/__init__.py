import sys
import os
"""
import inspect

# Ajout du repertoire au system pour facilter les import des modules
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
"""
sys.path.append(os.path.dirname(__file__))
