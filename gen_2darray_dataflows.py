import os
import csv
import pandas as pd
from collections import defaultdict

class CNNDataflowSpec:
    cnn_dimensions = ["k", "c", "r", "s", "x", "y"]
    weight_dimensions = ["k", "c", "r", "s"]
    output_dimensions = ["k", "x", "y"]
    
    directives_dimension_map = {
        "k": "(1, 1) K;\n",
        "c": "(1, 1) C;\n",
        "x": "(Sz(S),1) X;\n",
        "y": "(Sz(R),1) Y;\n",
        "r": "(Sz(R),Sz(R)) R;\n",
        "s": "(Sz(S),Sz(S)) S;\n",
    }
    spdim_dataflow_map = {
        "ws": ["kc", "kr"],
        "os": ["ky"],
        "nlr": ["kc"]
    }

class CNNDataflowGenerator(CNNDataflowSpec):
    spatial  = " " * 8 + "SpatialMap"
    temporal = " " * 8 + "TemporalMap"

    def _generate_dataflow(self, stationary, spatial_dims) -> None:
        if stationary == "ws":
            dimensions = self.weight_dimensions
        elif stationary == "os":
            dimensions = self.output_dimensions
        elif stationary == "nlr":
            dimensions = []
        else:
            print("Stationary type not supported ")
        
        dataflow_str = ""
        tp_outer_dims = [x for x in dimensions if x not in spatial_dims]
        for dim in tp_outer_dims:
            dataflow_str += self.temporal + self.directives_dimension_map[dim]
        for dim in spatial_dims:
            dataflow_str += self.spatial + self.directives_dimension_map[dim]
        
        tp_inner_dims = [x for x in self.cnn_dimensions if x not in dimensions and x not in spatial_dims]
        for dim in tp_inner_dims:
            dataflow_str += self.temporal + self.directives_dimension_map[dim]
        print(dataflow_str)
        return dataflow_str


    def _generate_files(self, stationary):
        parallel_dims = self.spdim_dataflow_map[stationary]

        path = "./tmp/"
        isExist = os.path.exists(path)
        if not isExist: os.makedirs(path)

        all_files = []
        for i in range(len(parallel_dims)):
            file_name = path + stationary + "_" + str(i) + ".m"
            file =  open(file_name, "w")
            file.write("Dataflow { \n")
            file.write(self._generate_dataflow(stationary, parallel_dims[i]))
            file.write("} \n")
            file.close()
            all_files.append(file_name.split("/")[-1].split(".")[0])
        return all_files
    
    def run_cmds(self, stationary):
        files = self._generate_files(stationary)

        for file in files:
            gen_run_cmd = "bash run_dataflows.sh " + file
            
            try:
                os.system(gen_run_cmd)
            except:
                print("cmd not work")
    
    def get_runtime_stats(self):
        path = "./tmp/csv/"
        arr = os.listdir(path)
        
        runtime_stats = defaultdict(list)
        for name in arr:
            df = pd.read_csv(path + name)
            runtime_stats[name].append(df[' Runtime (Cycles)'].tolist())
        
        for k, v in runtime_stats.items():
            print(k, v)


if __name__ == "__main__":
    stationary_types = ["ws", "os", "nlr"]

    generator = CNNDataflowGenerator()
    for type in stationary_types:
        print(type)
        generator.run_cmds(type)
        generator.get_runtime_stats()
