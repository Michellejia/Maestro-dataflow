import re
import argparse
import os.path
from argparse import RawTextHelpFormatter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('--model_file', type=str, default="dnn_model", help="<name of your model file with layer specs>")
    parser.add_argument('--dataflow_file', type=str, default="ws", help='dataflow choices: ws, os, nlr')
    parser.add_argument('--outfile', type=str, default="out.m", help='output file name')
    opt = parser.parse_args()
    print('Begin processing')
    base_path = '../../data/'
    if os.path.exists(base_path + 'model/' + opt.model_file):
        with open('../../artifacts/' + opt.dataflow_file + ".m" ,"r") as fd:
                with open(base_path + 'mapping/' + opt.outfile, "w") as fo:
                    with open(base_path + 'model/' + opt.model_file, "r") as fm:
                        for line in fm:
                            if(re.search("Dimensions",line)):
                                fo.write(line)
                                fd.seek(0)
                                fo.write(fd.read())
                            else:
                                fo.write(line)

        print("Mapping file created")
    else:
        print("Model file not found, please provide one")
