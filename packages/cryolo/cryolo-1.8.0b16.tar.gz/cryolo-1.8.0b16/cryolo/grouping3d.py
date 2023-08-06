import numpy as np
from cryolo import  utils

def convert_traces_to_bounding_boxes(traces):
    """
    Converts traces to a list of BoundingBox instances
    :param traces: Results of tracing
    :return: List of BoundingBox instances.
    """
    ccords = []
    for trace_id in np.unique(traces["particle"]):#range(num_particles):
        one_trace = traces[traces["particle"] == trace_id]

        xcoords = one_trace["x"].tolist()
        ycoords = one_trace["y"].tolist()
        zcoords = one_trace["frame"].tolist()
        widths = one_trace["widths"].tolist()
        heights = one_trace["heights"].tolist()
        confidence = one_trace["confidence"].tolist()
        est_box_widths = [meta["boxsize_estimated"][0] for meta in one_trace["meta"].tolist()]
        est_box_heights = [meta["boxsize_estimated"][1] for meta in one_trace["meta"].tolist()]

        x = np.mean(xcoords)
        y = np.mean(ycoords)
        z = np.round(np.mean(zcoords))
        w = np.mean(widths)
        h = np.mean(heights)
        c = np.mean(confidence)
        estimated_boxsize = (np.mean(est_box_widths),np.mean(est_box_heights))

        meta = {"boxsize_estimated": estimated_boxsize}
        meta["num_boxes"] = len(xcoords)
        bbox = utils.BoundBox(
            x=x,
            y=y,
            z=z,
            c=c,
            w=w,
            h=h,
            depth=w, # set it to same as the width. Should be a cube anyway.
            classes=[c]
        )
        bbox.meta = meta
        ccords.append(bbox)
    return ccords

def filaments_group_to_3D(filaments_df, window_size, box_distance):
    """
     For first filament: Subtract the first from
     last position and normalize the vector. This gives v0.
     v_avg = v0
     For each other filament
         Subtract(Last,First) and normalize -> v_k
         if v_k dot v_avg > 0:
           v_avg += v_k
           v_avg = norm(v_avg)
     Sort all filament positions along v_avg
     Running moving average along v_avg
     Resample


    :param filaments_df:
    :return:
    """

    def normalize_vec(vec):
        norm = np.linalg.norm(vec)
        if norm == 0:
            return vec
        return vec / norm

    def fila_to_vect(fil,start_minus_end=False):
        xs = fil["x"].tolist()
        ys = fil["y"].tolist()

        if start_minus_end:
            vec = np.array([xs[0]-xs[-1],ys[0]-ys[-1]])
        else:
            vec = np.array([xs[0]-xs[-1],ys[0]-ys[-1]])

        return normalize_vec(vec)

    nphelp = filaments_df["width"].to_numpy()
    same_box_size = (np.abs(nphelp-nphelp[0])<10**-6).all()

    assert same_box_size, print("The filaments have to have the same box size. Exit.")
    boxsize = nphelp[0]
    '''
    Calculate average direction v_avg of all filaments 
    '''
    fids = np.unique(filaments_df["fid"].tolist())

    v_avg = fila_to_vect( filaments_df[filaments_df["fid"] == fids[0]])
    for fid in fids[1:]:
        filament_trace = filaments_df[filaments_df["fid"] == fid]
        vec = fila_to_vect(filament_trace)
        if np.dot(vec,v_avg) < 0:
            vec = fila_to_vect(filament_trace,start_minus_end=True)
        v_avg = v_avg + vec
        v_avg = normalize_vec(v_avg)

    '''
     Sort them according their x,y coordinates.
    '''
    xs = []
    ys = []
    zs = []
    conf=[]

    for fid in fids:
        filament_trace = filaments_df[filaments_df["fid"] == fid]
        xs.extend(filament_trace["x"].tolist())
        ys.extend(filament_trace["y"].tolist())
        zs.extend(filament_trace["frame"].tolist())
        conf.extend(filament_trace["confidence"].tolist())


    xs = np.array(xs)
    ys = np.array(ys)
    zs = np.array(zs)
    conf = np.array(conf)

    dotproducts = []
    for i in range(len(xs)):
        dp = np.dot(
            v_avg,
            np.array([xs[i], ys[i]])
        )
        dotproducts.append(
            dp
        )
    dotproducts = np.array(dotproducts)
    sorted_coords_indicis = np.argsort(dotproducts)
    xs = xs[sorted_coords_indicis]
    ys = ys[sorted_coords_indicis]
    zs = zs[sorted_coords_indicis]
    conf = conf[sorted_coords_indicis]
    dotproducts = dotproducts[sorted_coords_indicis]

    '''
    Moving average
    '''
    w = window_size
    boxes_3d = []

    for i in range(int(min(dotproducts)),int(max(dotproducts))):
        window_elements = np.logical_and(dotproducts > (i-w/2), dotproducts<i+w/2)

        if np.sum(window_elements) > 0:
            x3d = np.mean(xs[window_elements])
            y3d = np.mean(ys[window_elements])
            z3d = int(np.mean(zs[window_elements]))
            conf3d = np.mean(conf[window_elements])
            boxes_3d.append(utils.BoundBox(x=x3d,y=y3d,z=z3d, w=boxsize,h=boxsize,depth=boxsize,c=conf3d))

    '''
    resample
    '''
    new_fil = utils.Filament(boxes=boxes_3d)
    resampled_filament = utils.resample_filaments([new_fil], box_distance)
    if len(resampled_filament) > 0:
        return resampled_filament[0]
    return None

def get_local_filament_direction(position, boxes, radius=2):

    from_i = max(0, position-radius)
    to_i = min(position+radius,len(boxes)-1)
    if from_i == to_i:
        return np.array([0,0])
    dx = boxes[from_i].x - boxes[to_i].x
    dy = boxes[from_i].y - boxes[to_i].y

    dvec = np.array([dx,dy])
    dvec = dvec / np.linalg.norm(dvec)
    return dvec



def do_tracing_filaments(filaments_dict,
               search_range=5,
               memory=3,
               confidence_threshold=0,
               min_edge_weight=0,
               window_size=2,
               box_distance=1):
    import pandas as pd
    import trackpy as tp
    coords_and_frame = {
        "x": [],
        "y": [],
        "frame": [],
        "fid": [],
        "confidence":[],
        "width":[],
        "height":[],
        "meta":[],
        "fdirection":[]
    }
    fid = 0
    num_box = 0

    for frame_number in filaments_dict:
        resampled_filaments = utils.resample_filaments(filaments_dict[frame_number],2*search_range+1)
        for filament in resampled_filaments:
            for box_i, box in enumerate(filament.boxes):
                if box.c > confidence_threshold:
                    coords_and_frame["x"].append(box.x)
                    coords_and_frame["y"].append(box.y)
                    coords_and_frame["frame"].append(frame_number)
                    coords_and_frame["fid"].append(fid)
                    coords_and_frame["confidence"].append(box.c)
                    coords_and_frame["meta"].append(box.meta)
                    coords_and_frame["width"].append(box.w)
                    coords_and_frame["height"].append(box.h)
                    coords_and_frame["fdirection"].append(get_local_filament_direction(position=box_i, boxes=filament.boxes, radius=2))
                    num_box = num_box + 1
            fid = fid + 1
    if len(coords_and_frame["x"])==0:
        return []
    coords_frame_df = pd.DataFrame(coords_and_frame)
    tp.quiet(True)
    #import trackpy.linking as lnkng
    #lnkng.linking.Linker.MAX_SUB_NET_SIZE=50
    '''
    print("memory", memory)
    print("searchrange", search_range)
    print("windowsize", window_size)
    print("min_edge", min_edge_weight)
    print("conf", confidence_threshold)
    print("widht", coords_frame_df["width"][0])
    print("maxmin", np.max(coords_frame_df["x"]),np.min(coords_frame_df["x"]))
    '''
    #print("SUBETCONF:", lnkng.linking.Linker.MAX_SUB_NET_SIZE,lnkng.linking.Linker.MAX_SUB_NET_SIZE_ADAPTIVE, memory*search_range+1)
    coords_frame_traced_df = tp.link_df(coords_frame_df,
                                        search_range=search_range,
                                        adaptive_stop = 2,
                                        adaptive_step = 0.8,
                                        memory=memory)

    #print("Linking done")

    # Next steps:
    # Build graph
    #np.unique(coords_frame_traced_df["particle"])
    import networkx as nx
    G = nx.Graph()
    edges = []
    nodes = []
    all_r_values = []
    for trace_id in np.unique(coords_frame_traced_df["particle"]):
        one_trace = coords_frame_traced_df[coords_frame_traced_df["particle"] == trace_id]
        filament_directions = one_trace["fdirection"].tolist()
        exceeded = False

        for i in range(len(filament_directions)-1):
            r = np.linalg.norm(np.cross(filament_directions[i],filament_directions[i+1]))
            all_r_values.append(r)
            if r > 0.15:
                exceeded = True
        if exceeded:
            continue


        trace_fid_list = one_trace["fid"].tolist()
        for i in range(len(trace_fid_list)-1):
            edge = sorted((trace_fid_list[i],trace_fid_list[i+1]))
            edges.append(edge)
        nodes.extend(trace_fid_list)

    # Add nodes + Calculate edge weight + add weights
    nodes = set(nodes)
    for node in nodes:
        G.add_node(node)

    for edge in edges:
        edge_weight = len([i for i,an_edge in enumerate(edges) if an_edge == edge])

        fil_length_a = len(coords_frame_traced_df[coords_frame_traced_df["fid"] == edge[0]])
        fil_length_b = len(coords_frame_traced_df[coords_frame_traced_df["fid"] == edge[1]])
        edge_weight = edge_weight/min(fil_length_a,fil_length_b)

        has_minimum_weight = edge_weight > min_edge_weight

        if has_minimum_weight:
            G.add_edge(edge[0],edge[1],weight=edge_weight)

    # Find connected components


    connected_components = nx.connected_components(G)

    # Generate one 3D trace per connected component
    filaments_3d = []
    for sub in connected_components:
        filaments_of_cc = coords_frame_traced_df[ coords_frame_traced_df["fid"].isin(sub)]
        if len(filaments_of_cc.index) > 1:
            f3d = filaments_group_to_3D(filaments_of_cc, window_size=window_size, box_distance=box_distance)
            if f3d is not None:
                filaments_3d.append(f3d)

    #print("NUMBER OF FILS (TOTAL):", nx.algorithms.components.number_connected_components(G))
    #print("NUMBER OF FILS (FITERED):", num_components)



    return filaments_3d

def do_tracing(boxes_dict,
               search_range=5,
               memory=3,
               confidence_threshold=0,
               min_length=5):
    """
    Will trace the boxes

    :param boxes_dict: Dictonary of lists of BoundingBox instances. Key the is the frame number.
    :param search_range: Maximum distance between position to get linked
    :param memory: Maximum gap in z direction.
    :param min_length: Minimum number of points (boxes in one  trace (default 5)
    :param confidence_threshold: Ignores boxes in boxes_list which have a confidence lower than this threshold
    :return: List of 3D bounding boxes
    """
    import pandas as pd
    import trackpy as tp
    coords_and_frame = {"x": [], "y": [], "frame": []}
    confidences = []
    meta = []
    widths = []
    heights = []
    for frame_number  in boxes_dict:
        for box in boxes_dict[frame_number]:
            if box.c > confidence_threshold:
                coords_and_frame["x"].append(box.x)
                coords_and_frame["y"].append(box.y)
                coords_and_frame["frame"].append(frame_number)
                confidences.append(box.c)
                meta.append(box.meta)
                widths.append(box.w)
                heights.append(box.h)
                assert len(box.classes) == 1, "for classes > 1 we need to complete the implementation"
    if len(coords_and_frame["x"])==0:
        return []
    coords_frame_df = pd.DataFrame(coords_and_frame)

    tp.quiet(True)
    coords_frame_traced_df = tp.link_df(coords_frame_df,
                                       search_range=search_range,
                                       memory=memory)
    coords_frame_traced_df["confidence"] = confidences
    coords_frame_traced_df["meta"] = meta
    coords_frame_traced_df["widths"] = widths
    coords_frame_traced_df["heights"] = heights
    coords_frame_traced_df= tp.filter_stubs(coords_frame_traced_df, min_length)
    boxes = convert_traces_to_bounding_boxes(coords_frame_traced_df)
    return boxes

def do_cluster(boxes_list,max_dist=2,max_z=3, confidence_threshold=0.3):

    num_boxes = np.sum([len([box for box in boxes if box.c>confidence_threshold]) for boxes in boxes_list])

    data = np.zeros(shape=(num_boxes,3))
    k = 0
    for boxes_index, boxes in enumerate(boxes_list):
        for box in boxes:
            if box.c > confidence_threshold:
                data[k,0]=box.x
                data[k,1]=box.y
                data[k,2]=boxes_index
                k = k + 1
    from sklearn import cluster
    epsilon = np.sqrt(max_dist * max_dist + max_z * max_z)

    clustering = cluster.AgglomerativeClustering(n_clusters=None, distance_threshold=80).fit(data) #cluster.DBSCAN(eps=epsilon, min_samples=3).fit(data)

    print("Num clusters found:", len(set(clustering.labels_)))

    return None#NotImplementedError("This method is not implemented yet")
