import numpy
import pandas
import csv
import sys,getopt
import os


class Read_Format_input:
    def __init__(self, reference_file, input_file):
        self.reference_file = reference_file
        self.input_file = input_file

    def reader(self):
        read_reference = pd.read_csv(self.reference_file, sep=('\t'))
        read_input = pd.read_csv(self.input_file, sep=('\t'))
       
        read_input.columns = ['AccNum','Run', 'AlleleLength']
        #For comparison, you want the reference and input file to have the same columns names for when you merge, so rename the columns specified
        #Ex: read_input.rename(columns={'AlleleLength':'length'}, inplace = True)
        read_input.rename(columns={'AlleleLength':'Length'})
       
        #Filter columns you may want to seperate from the original dataframe.
        #Example df_reference = read_reference[['Gene', 'Run']]
        df_reference = read_reference[['AccNum', 'Run']]
        df_input = read_input[['AccNum', 'Run']]
       
        df_reference_formated, df_input_formated = self.formating(df_reference, df_input)
       
        return (df_reference_formated, df_input_formated)

    def formating(self, df_reference, df_input):
        df_reference.loc[:,'Run'] = df_reference.Run.str.strip('Run:')
        df_reference.loc[:,'Run'] = df_reference.Run.apply(lambda x:int(x))
        df_input.loc[:,'Run'] = df_input.Run.str.strip('Run:')
        df_input.loc[:,'Run'] = df_input.Run.apply(lambda x:int(x))
       
        df_reference_sorted = df_reference.sort_values(by=['AccNum','Run'], inplace = False)
        df_input_sorted = df_input.sort_values(by=['AccNum','Run'], inplace = False)

        return (df_reference_sorted, df_input_sorted)

class Iteration_Index:
    def iterate(self, df_reference_sorted, df_input_sorted):
        for i in df_reference_sorted.index[:-1]:
            ref_row_1 = df_reference_sorted.ix[i]
            ref_row_2 = df_reference_sorted.ix[i+1]
            #You can add some function after this or specify a different way to index through the dataframe.
            df_reference_sorted.ix[i, 'AccNum'] = Annotate.add_annotation(ref_row_1,ref_row_2)

       
        for i in df_input_sorted.index[:-1]:
            in_row_1 = df_input_sorted.ix[i]
            in_row_2 = df_input_sorted.ix[i+1]
            df_input_sorted.ix[i, 'AccNum'] = Annotate.add_annotation(in_row_1,in_row_2)

class Annotate:
    def add_annotation(self, row_1, row_2):
        if row_1['AccNum'] == row_2['AccNum']:
            if row_1['Length'] <= row_2['Length']:
                annotation = row_1['AccNum'] + '_S'
            else:
                annotation = row_1['AccNum'] + '_L'
        else:
            annotation = row_1['AccNum'] + '_L'

        return annotation

class Merger:
    def merging_sort(self, df_reference_merging, df_input_merging):
        merged_df = df_reference_merging.merge(df_input_merging, left_on = 'AccNum', right_on = 'AccNum', how = 'inner')
        merged_df_sorted = merged_df.sort_values(by = ['AccNum'], inplace = False)
       
        return merged_df_sorted

class Validate:
    def validation(self, final_df):
        final_df['Match'] = np.where(final_df['Length_x'] == final_df['Length_y']) | ((final_df['Length_x'] - 1) == final_df['Length_y']),True, np.nan))
        No_Match = final_df[final_df.isnull().any(axis=1)]

        print(final_df)
        print('\n')
        print(No_Match)

class main(argv):
    reference_file = ''
    input_file = ''

    try:
        opts,args = getopt.getopt(argv, 'hr:i',['reference_file=','input_file='])
    except getopt.GetoptError:
        print('compare_template.py -r <reference_file> -i <input_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('compare_template.py -r <reference_file> -i <input_file>')
            sys.exit()
        elif opt in ('-r'):
            reference_file = arg
        elif opt in ('-i'):
            input_file = arg

    Read_ref, Read_input = Read_Format_input(reference_file, input_file).reader()
    Annotated_ref, Annotated_input = Iteration_Index().iterate(Read_ref, Read_input)
    Merge_dataframe = Merger().merging_sort(Annotated_ref, Annotated_input)
    Validate_Match = Validate().validation(Merge_dataframe)

if __name__ == "__main__":
    main(sys.argv[1:])
