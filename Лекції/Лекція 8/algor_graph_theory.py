# модель динаміки у системі
import matplotlib
from numpy.random import random
import networkx as nx
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')


def initialize():
    global G, nextG
    G = nx.karate_club_graph()
    G.pos = nx.spring_layout(G)

    for i in G.nodes:
        G.nodes[i]['state'] = 1 if random() > 0.5 else 0

    nextG = G.copy()

def observe():
    global G, nextG
    plt.cla()
    # Формуємо список кольорів на основі стану
    colors = ['red' if G.nodes[i]['state'] == 1 else 'blue' for i in G.nodes]

    nx.draw(G,  vmin=0, vmax=1, node_color=colors, pos=G.pos, with_labels=False)


def update():
    global G, nextG

    for i in G.nodes():
        count = G.nodes[i]['state']
        for j in G.neighbors(i):
            count += G.nodes[j]['state']

        ratio = count/(G.degree(i)+1)

        if ratio > 0.5:
            nextG.nodes[i]['state'] = 1
        elif ratio < 0.5:
            nextG.nodes[i]['state'] = 0
        else:
            nextG.nodes[i]['state'] = 1 if random() < .5 else 0

        G, nextG = nextG, G


import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])


