# generate model mapping file
cd tools/frontend
python3 modelfile_to_mapping.py --model_file alexnet.m --dataflow_file $1 --outfile $1.m
cd ../..

# run mapping file
echo "==="$1"==="
./maestro --HW_file='data/hw/accelerator_1.m' \
        --Mapping_file='data/mapping/'$1'.m' \
        --print_res=false \
        --print_res_csv_file=true \
        --print_log_file=false

mkdir -p ./artifacts/csv
mv *.csv ./artifacts/csv