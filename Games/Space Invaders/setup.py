from cx_Freeze import setup, Executable
import sys
import pygame,random

#executables = [cx_Freeze.Executable("invaders.py", base=base)]

setup(
    name = "gamev2.py",
    version = "0.1",
    options = {'build_exe':{'packages':['pygame','random','time'],'include_files':[]}},
    discription = 'Simulation of space invaders',
    executables = [Executable("gamev2.py")]
    )

