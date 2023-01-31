import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff 

alpha = 220
color_palette = ['red', 'green', 'blue', 'purple', 'yellow', 'cyan', 'brown', 'pink', 'black', 'blueviolet', 'burlywood', 'cadetblue']

def set_fig(traces, filename, save, has_bg=False):
    
    fig = go.Figure(data=traces)

    for trace in fig['data']: 
        trace['showlegend'] = False

    camera = dict(
    up=dict(x=0, y=1, z=0),
    center=dict(x=0, y=0, z=0),
    eye=dict(x=1.0, y=1.0, z=1.0)
    )

    fig.update_layout(scene_camera=camera)

    range_min = -2.0
    range_max = 2.0

    if has_bg:
        fig.update_layout(
            scene = dict(xaxis = dict(range=[range_min,range_max],),
                        yaxis = dict(range=[range_min,range_max],),
                        zaxis = dict(range=[range_min,range_max],),
                        aspectmode='cube'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title=filename,
            autosize=False,width=1000,height=1000)
    else:
        fig.update_layout(
            scene = dict(xaxis = dict(range=[range_min,range_max],),
                        yaxis = dict(range=[range_min,range_max],),
                        zaxis = dict(range=[range_min,range_max],),
                        aspectmode='cube'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title=filename,
            autosize=False,width=1000,height=1000)

    #fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    
    if save is True:
        fig.write_image(filename)
    else:
        fig.show()

def display_pcs(pcs, filename=' ', save=False):

    traces = []
    all_x = []
    all_y = []
    all_z = []
    for i in range(len(pcs)):
        x = []
        y = []
        z = []
        c = []
        for p in pcs[i]:
            c.append(color_palette[i%len(color_palette)])
            x.append(p[0])
            if len(p) > 1:
                y.append(p[1])
            else:
                y.append(0.0)
            if len(p) > 2:
                z.append(p[2])
            else:
                z.append(0.0)

        trace = go.Scatter3d(
            x=x, 
            y=y, 
            z=z, 
            mode='markers', 
            marker=dict(
                size=3,
                color=c,                
                colorscale='Viridis',   
                opacity=1.0
            )
        )
        traces.append(trace)
        all_x += x
        all_y += y
        all_z += z
    
    set_fig(traces, filename, save)