# модель виборця
import matplotlib
from numpy.random import random, choice
# from random import choice
import networkx as nx
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')


def initialize():
    global G
    G = nx.karate_club_graph()
    G.pos = nx.spring_layout(G)

    for i in G.nodes:
        G.nodes[i]['state'] = 1 if random() < .5 else 0

def observe():
    global G
    plt.cla()
    # Формуємо список кольорів на основі стану
    colors = ['green' if G.nodes[i]['state'] == 1 else 'plum' for i in G.nodes]

    nx.draw(G,  vmin=0, vmax=1, node_color=colors, pos=G.pos, with_labels=False)


def update():
    global G

    listener = choice(list(G.nodes()))
    speaker = choice(list(G.neighbors(listener)))

    G.nodes[listener]['state'] = G.nodes[speaker]['state']


import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])


