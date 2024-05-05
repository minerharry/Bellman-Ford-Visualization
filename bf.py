
#original code from https://github.com/stevenhalim/cpbook-code
#modified to add named vertices
from typing import DefaultDict, Generator
import matplotlib.animation
from netgraph import InteractiveGraph
import networkx as nx
import matplotlib.pyplot as plt

#yields either none or: loop number, active edge
def main(g:nx.Graph)->Generator[None|tuple[int,tuple[str,str]|None],None,None]:
    INF = int(1e9)

    # Graph in Figure 4.18, has negative weight, but no negative cycle
    # 5 5 0
    # 0 1 1
    # 0 2 10
    # 1 3 2
    # 2 3 -10
    # 3 4 3

    # Graph in Figure 4.19, negative cycle exists, Bellman Ford's can detect this
    # 3 3 0
    # 0 1 1000
    # 1 2 15
    # 2 1 -42

    f = open("bf2.txt", "r")

    #first line: size of vertices, edges, starting node
    V, E, s = f.readline().strip().split(" ");
    V,E = map(int,(V,E));

    #adjacency list
    AL = DefaultDict[str,list[tuple[str,int]]](lambda: []);

    #edge list
    EL:list[tuple[str,str,int]] = [];
    for _ in range(E):
        #start, end, weight
        u, v, w = f.readline().split(" ");
        AL[u].append((v, int(w)));
        EL.append((u,v,int(w)));
    
    g.add_weighted_edges_from(EL);
    g.add_nodes_from(((v,{"distory":["inf"]}) for v in g));
    yield None;

    #vertex list
    VL = list(g);    
    

    EL.sort(key=lambda e: e[2]); #sort based on edge weight

    # Bellman Ford's routine, basically = relax all E edges V-1 times
    dist = {v:INF for v in VL}               # INF = 1e9 here
    dist[s] = 0
    # print(g[s])
    for i in range(0, V-1):                      # total O(V*E)
        for u,v,w in EL:
            assert (u,v) in g.edges
            yield i,(u,v);
            if (not dist[u] == INF):
                if (dist[u] + w >= dist[v]): continue;
                dist[v] = dist[u]+w;
                print(v);
                print(v,g.nodes[v]['distory']);
                g.nodes[v]['distory'].append(str(dist[v]));
                print(v,g.nodes[v]['distory']);
                #TODO: update graph info
                yield i,(u,v);

    hasNegativeCycle = False
    for u in VL:                        # one more pass to check
        if (not dist[u] == INF):
            for v, w in AL[u]:
                if (dist[v] > dist[u] + w):      # should be false
                    hasNegativeCycle = True      # if true => -ve cycle
    print("Negative Cycle Exist? {}".format("Yes" if hasNegativeCycle else "No"))

    if (not hasNegativeCycle):
        for u in VL:
            print("SSSP({}, {}) = {}".format(s, u, dist[u]))

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(6,4));
    G = nx.DiGraph();

    gen = main(G);
    # pos = None;

    displayGraph = None;

    edge_alpha = DefaultDict(lambda: 0.8);
    edge_z = DefaultDict(lambda: 1);
    node_size = DefaultDict(lambda: 3);

    def update(num):        
        out = next(gen);
        idx,edge = out if out else (0,None)
        global displayGraph
        displayGraph = displayGraph or InteractiveGraph(G,ax=ax,edge_width=2,edge_color='black',edge_layout='arc',arrows=True,node_labels=True,edge_labels={e:G.edges[e]['weight'] for e in G.edges});

        # displayGraph.draw_edges(
        #     displayGraph.edge_paths,
        #     {e:0.01 if e != edge else 0.02 for e in displayGraph.edge_paths},
        #     {e:'black' if e != edge else 'orange' for e in displayGraph.edge_paths},edge_alpha,edge_z,True,node_size);

        for e,artist in displayGraph.edge_artists.items():
            print(artist.width)
            if edge and e == edge:
                artist.update_width(0.02);
                artist.facecolor='orange';
            else:
                artist.update_width(0.01);
                artist.facecolor='black';

        ax.figure.canvas.draw_idle();
        
            # artist._update_path();
        # ax.figure.draw

        # return displayGraph.edge_artists.values()

        # ax.clear();
        # nx.draw_networkx_edges(G, pos=pos, ax=ax, edge_color="gray",width=2,label=False,connectionstyle='arc3,rad=0.1');
        # nx.draw_networkx_nodes(G, pos=pos, ax=ax,label=False,node_size=size);

        # if edge:
        #     nx.draw_networkx_edges(G,pos=pos,ax=ax,edgelist=[edge],width=8,edge_color="orange",alpha=0.5,label=False,arrows=False,connectionstyle='arc3,rad=0.1');
        # nx.draw_networkx_labels(G,pos=pos,ax=ax);
        # nx.draw_networkx_labels(G,pos={n:(p[0],p[1]-0.1) for n,p in pos.items()},ax=ax,labels={n:a['distory'][-1] for n,a in G.nodes.items()},verticalalignment='top',font_color='green')
        # nx.draw_networkx_labels(G,pos={n:(p[0],p[1]-0.2) for n,p in pos.items()},ax=ax,labels={n:", ".join(a['distory'][:-1]) for n,a in G.nodes.items()},verticalalignment='top',font_color='red')
        # nx.draw_networkx_edge_labels(G,pos=pos,ax=ax,edge_labels={e:a['weight'] for e,a in G.edges.items()},connectionstyle='arc3,rad=0.1')

        # ax.set_title("Frame %d:    "%(num+1) +  f"Loop Index {idx}" + (f" - Active Edge {edge}" if edge else ""), fontweight="bold")
        # ax.set_xticks([])
        # ax.set_yticks([])

    ani = matplotlib.animation.FuncAnimation(fig, update, interval=1000, repeat=True)
    plt.show()