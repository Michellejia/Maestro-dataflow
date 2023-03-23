import argparse
import subprocess

argParser = argparse.ArgumentParser()
argParser.add_argument("-m", "--mapping_file", help="path to the mapping file")

# num_pes: 256
# l1_size_cstr: 100
# l2_size_cstr: 3000
# noc_bw_cstr: 1000
# offchip_bw_cstr: 50
args, leftovers = argParser.parse_known_args()

pe_s_range = [2**x for x in range(4,14)]
l1_size_range = [100]
l2_size_range = [3000]
noc_bw = 1000
offchip_bw= 50

hardware_list = []

for pe_s in pe_s_range:
    for l1_size in l1_size_range:
        for l2_size in l2_size_range:
            print(f"generating accelerator hardware with pe = {pe_s}, l1 = {l1_size}, l2 = {l2_size}")
            hardware_file_name = f"data/hw/accelerator_p{pe_s}_l{l1_size}_{l2_size}.m"
            hardware_list.append(hardware_file_name)
            with open(hardware_file_name,"w") as f:
                f.write(f"num_pes: {pe_s}\n")
                f.write(f"l1_size_cstr: {l1_size}\n")
                f.write(f"l2_size_cstr: {l2_size}\n")
                f.write(f"noc_bw_cstr: {noc_bw}\n")
                f.write(f"offchip_bw_cstr: {offchip_bw}\n")
         
if args.mapping_file is not None:
    print(args.mapping_file)
    for hardware in hardware_list:
        sim_command = f"./maestro --HW_file={hardware} \
            --Mapping_file={args.mapping_file} \
            --print_res=false \
            --print_res_csv_file=true \
            --print_log_file=false"
        subprocess.run(sim_command,shell=True)
        target_csv_path = hardware.replace(".m",".csv")
        target_csv_path = target_csv_path.replace("data/hw/","artifacts/run_results/")
        generated_csv_filename = args.mapping_file.split("/")[-1].replace(".m",".csv")
        target_csv_path = target_csv_path.replace("accelerator",generated_csv_filename.split(".")[0])
        move_command = f"mkdir -p ./artifacts/run_results && mv {generated_csv_filename} {target_csv_path}"
        subprocess.run(move_command,shell=True)

