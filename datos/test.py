import pandas as pd
import h2o

h2o.init()

data = {'sexo': 1, 'tos': 1, 'fiebre': 0,
         'fatiga': 1, 'dificultad_respiratoria': 1, 'odinofagia': 0,
         'rinorrea': 1, 'diarrea': 0, 'cefalea': 0}
# Create the pandas DataFrame
df = pd.DataFrame(data, index=[0])
data_h = h2o.H2OFrame(df)
saved_model = h2o.load_model("Model/GBM_grid_1_AutoML_1_20211218_122220_model_106")
prediccion = saved_model.predict(data_h)

data_as_df = prediccion.as_data_frame()
result = data_as_df.iloc[0,2]

print("---->"+ str(result))