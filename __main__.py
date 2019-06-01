import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True, help='Enter the input file you want to compare versus the reference.')
    parser.add_argument('-r', '--reference', required=True, help='Enter reference file.')
    args = parser.parse_args()

    Read_ref, Read_input = Read_Format_input(args.reference, args.input_file).reader()

    Annotated_ref, Annotated_input = Iteration_Index().iterate(Read_ref, Read_input)
    Merge_dataframe = Merger().merging_sort(Annotated_ref, Annotated_input)
    Validate_Match = Validate().validation(Merge_dataframe)

if __name__ == "__main__":
    main()
