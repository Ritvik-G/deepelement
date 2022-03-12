import pandas
pandas.read_json("reports.jl", lines=True ).to_excel("Filename.xlsx") #Converts the given json lines file to xlsx for better viewability.
