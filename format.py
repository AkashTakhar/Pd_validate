import numpy
import pandas

#Or change the the class name to File_Data
class File_Format(Object):
    def __init__(self, **kwargs):
        allowed_inputs = set(['reference', 'input_file'])
        self.__dict__.update((key, False) for key in allowed_inputs)
        self.__dict__.update((key, value) for key, value in kwargs.items() if key in allowed_inputs)

    def read_file(self):
        reference_data = pd.read_csv(self.reference, sep='\t')
        input_file_data = pd.read_csv(self.input_file, sep='\t')

        #Add a system here to take specified information from a configuration file and columns.
        #read_input.columns = ['AccNum','Run', 'AlleleLength']
        input_file_data.columns = []
        reference_data.columns = []

        #If columns in one dataframe dont match have a system to rename them.
        #ex: read_input.rename(columns={'AlleleLength':'Length'})
        input_file.rename = []

        #If you want to seperate a dataframe more.
        #ex: df_reference = read_reference[['AccNum', 'Run']]

        #pass the dataframes to a method for formating the file or think about creating anouther module program to handle that.
        #ex: df_reference_formated, df_input_formated = self.formating(df_reference, df_input)

        return (reference_data, input_file_data)
