import os
import re
import math
import pandas as pd
import numpy as np
from collections import defaultdict

class CNNDataflowSpec:
    cnn_dimensions = ["K", "C", "R", "S", "X", "Y"]
    weight_dimensions = ["K", "C", "R", "S"]
    output_dimensions = ["K", "X", "Y"]
    
    directives_dimension_map = {
        "K": "(1, 1) K;\n",
        "C": "(1, 1) C;\n",
        "X": "(Sz(S),1) X;\n",
        "Y": "(Sz(R),1) Y;\n",
        "R": "(Sz(R),Sz(R)) R;\n",
        "S": "(Sz(S),Sz(S)) S;\n",
    }
    spdim_dataflow_map = {
        "ws": ["KC", "KR", "CK", "CR", "RS", "SR"],
        "os": ["KY", "YK", "XY"],
        "nlr": ["KC", "CK"]
    }

class CNNDataflowGenerator(CNNDataflowSpec):
    spatial  = " " * 8 + "SpatialMap"
    temporal = " " * 8 + "TemporalMap"

    def __init__(self):
        self.best_dataflow = defaultdict(list)
        self.model_info = defaultdict(list)
        self.layer_length = 0

    def _generate_dataflow(self, stationary, spatial_dims, add_cluster) -> None:
        if stationary == "ws":
            dimensions = self.weight_dimensions
        elif stationary == "os":
            dimensions = self.output_dimensions
        elif stationary == "nlr":
            dimensions = self.cnn_dimensions
        else:
            print("Stationary type not supported ")
        
        dataflow_str = ""
        tp_outer_dims = [x for x in dimensions if x not in spatial_dims]
        for dim in tp_outer_dims:
            dataflow_str += self.temporal + self.directives_dimension_map[dim]
 
        # dataflow_str += " " * 8 + "Cluster(5, P);\n"
        first_loop = False
        for dim in spatial_dims:
            dataflow_str += self.spatial + self.directives_dimension_map[dim]
            if add_cluster and not first_loop:
                dataflow_str += " " * 8 + "Cluster(" + str(self.best_dataflow[stationary][0]) + ", P);\n"
                first_loop = True

        tp_inner_dims = [x for x in self.cnn_dimensions if x not in dimensions and x not in spatial_dims]
        for dim in tp_inner_dims:
            dataflow_str += self.temporal + self.directives_dimension_map[dim]
        return dataflow_str


    def _generate_files(self, stationary):
        parallel_dims = self.best_dataflow[stationary][1]

        path = "./artifacts/"
        isExist = os.path.exists(path)
        if not isExist: os.makedirs(path)

        file_name = path + stationary + ".m"
        file =  open(file_name, "w")
        file.write("Dataflow { \n")
        file.write(self._generate_dataflow(stationary, parallel_dims, True))
        file.write("} \n")
        file.close()
        
        file_name = file_name.split("/")[-1].split(".")[0]
        return file_name
    
    def _process_model_file(self, model):
        """
        Get k, c, r, s, x, y, and stride of each layer
        """
        self.model_info = defaultdict(list)
        with open(model, 'r') as f:
            lines = f.readlines()

            for line in lines:
                res = re.findall(r'\{.*?\}', line)
                if line.startswith("Stride"):
                    res = res[0][1:-1]
                    stride = res.split(",")[0].split(":")
                    self.model_info["stride"].append(int(stride[1]))
                if line.startswith("Dimensions"):
                    res = res[0][1:-1]
                    segs = res.split(",")
                    for i in range(len(segs)):
                        segs[i] = segs[i].strip()

                    info = ["K", "C", "R", "S", "Y", "X"]
                    for i in range(len(info)):
                        self.model_info[info[i]].append(int(segs[i][segs[i].find(info[i]) + 3:]))
        
        self.layer_length = len(self.model_info['K'])
        stride_num = len(self.model_info['stride'])
        if stride_num < self.layer_length:
            self.model_info['stride'] = np.concatenate([self.model_info['stride'], np.ones(self.layer_length - stride_num)])

        for i in range(self.layer_length):
            self.model_info["Ox"].append(int((self.model_info["X"][i] - self.model_info["R"][i]) / self.model_info["stride"][i] + 1))
            self.model_info["Oy"].append(int((self.model_info["Y"][i] - self.model_info["S"][i]) / self.model_info["stride"][i] + 1))
        # print(self.model_info)
    
    def calculate_best_dataflow(self, stationary_type):
        """
        Get the best dataflow by maximizing average PE utilization of different layers
            # of clusters in total (cluster_num) = min(# PE / cluster_size, outer_dim)
            # of clusters needed for inner loop (cluster_num_inner) = ceil(inner_dim / cluster_size)
            PE utilization per cluster (PE_utilization_per_cluster) = inner_dim / (cluster_num_inner * cluster_size)
            
            PE utilization = PE_utilization_per_cluster * cluster_size * cluster_num
                           = inner_dim / ceil(inner_dim / cluster_size) * min(# PE / cluster_size, outer_dim)

            design points: cluster_size, inner/outer_dim
        """
        clusters = [4, 8, 16, 32, 64, 128, 256]
        outer_inner_dimension = self.spdim_dataflow_map[stationary_type]

        model = "./data/model/alexnet.m"
        
        if len(self.model_info) == 0:
            self._process_model_file(model)

        PE_utilization = [0 for i in range(self.layer_length)]
        for cluster in clusters:
            for outer_inner in outer_inner_dimension:
                curr_PE_utilization = 0
                for i in range(self.layer_length):
                    outer_dim, inner_dim = self.model_info[outer_inner[0]][i], self.model_info[outer_inner[1]][i]
                    curr_PE_utilization += inner_dim / math.ceil(inner_dim / cluster) * min(256 / cluster, outer_dim)

                if curr_PE_utilization > PE_utilization[i]:
                    PE_utilization[i] = curr_PE_utilization
                    self.best_dataflow[stationary_type] = [cluster, outer_inner]
        print(self.best_dataflow)
    
    def run_cmds(self, stationary):
        file = self._generate_files(stationary)

        gen_run_cmd = "bash run_dataflows.sh " + file
        
        try:
            os.system(gen_run_cmd)
        except:
            print("cmd not work")
    
    def get_runtime_stats(self):
        path = "./artifacts/csv/"
        arr = os.listdir(path)
        
        runtime_stats = defaultdict(list)
        for name in arr:
            df = pd.read_csv(path + name)
            runtime_stats[name].append(df[' Runtime (Cycles)'].tolist())
        
        return runtime_stats


if __name__ == "__main__":
    stationary_types = ["ws", "os", "nlr"]

    generator = CNNDataflowGenerator()
    for type in stationary_types:
        generator.calculate_best_dataflow(type)
        print(type)
        generator.run_cmds(type)
        stats = generator.get_runtime_stats()

        for k, v in stats.items():
            print(k, v)
